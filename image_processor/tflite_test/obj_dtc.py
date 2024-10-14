import argparse
import sys
import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils import visualize

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()

def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int) -> None:
    """Chạy inference liên tục trên các ảnh thu được từ camera, chỉ nhận diện người.

    Args:
        model: Tên của mô hình TFLite để nhận diện đối tượng.
        max_results: Số lượng kết quả nhận diện tối đa.
        score_threshold: Ngưỡng điểm số của các kết quả nhận diện.
        camera_id: ID của camera để truyền vào OpenCV.
        width: Chiều rộng của khung hình từ camera.
        height: Chiều cao của khung hình từ camera.
    """

    # Bắt đầu thu video từ camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    detection_frame = None

    # Khởi tạo mô hình nhận diện đối tượng
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           running_mode=vision.RunningMode.IMAGE,
                                           max_results=max_results, score_threshold=score_threshold)
    detector = vision.ObjectDetector.create_from_options(options)

    # Chụp ảnh liên tục từ camera và chạy nhận diện
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.resize(image, (640, 480))
        if not success:
            sys.exit('ERROR: Không thể đọc từ webcam. Vui lòng kiểm tra cấu hình webcam.')

        image = cv2.flip(image, 1)

        # Chuyển đổi ảnh từ BGR sang RGB như yêu cầu của mô hình TFLite.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Chạy nhận diện đối tượng sử dụng mô hình (đồng bộ).
        detection_result = detector.detect(mp_image)

        # Chỉ giữ lại các đối tượng là người (person)
        human_results = [detection for detection in detection_result.detections if detection.categories[0].category_name == 'person']

        # Hiển thị FPS
        fps_text = 'FPS = {:.1f}'.format(FPS)
        text_location = (left_margin, row_size)
        current_frame = image
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                    font_size, text_color, font_thickness, cv2.LINE_AA)

        # Chỉ hiển thị bounding box nếu có đối tượng người trong danh sách kết quả
        if human_results:
            detection_result.detections = human_results  # Cập nhật danh sách kết quả chỉ với các đối tượng là người
            current_frame = visualize(current_frame, detection_result)
            detection_frame = current_frame
        else:
            detection_frame = image  # Không có đối tượng nào được nhận diện, hiển thị khung hình gốc

        if detection_frame is not None:
            cv2.imshow('object_detection', detection_frame)

        # Tính toán FPS
        COUNTER += 1
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        # Dừng chương trình nếu nhấn phím ESC.
        if cv2.waitKey(1) == 27:
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Đường dẫn đến mô hình nhận diện đối tượng.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--maxResults',
        help='Số lượng kết quả nhận diện tối đa.',
        required=False,
        default=5)
    parser.add_argument(
        '--scoreThreshold',
        help='Ngưỡng điểm số của các kết quả nhận diện.',
        required=False,
        type=float,
        default=0.25)
    parser.add_argument(
        '--cameraId', help='ID của camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Chiều rộng của khung hình từ camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Chiều cao của khung hình từ camera.',
        required=False,
        type=int,
        default=480)
    args = parser.parse_args()

    run(args.model, int(args.maxResults),
        args.scoreThreshold, int(args.cameraId), args.frameWidth, args.frameHeight)

if __name__ == '__main__':
    main()
