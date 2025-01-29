import argparse
import sys
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

COUNTER, FPS = 0, 0
START_TIME = time.time()

def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int) -> None:

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    fps_avg_frame_count = 10
    detection_result_list = []

    def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME

        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        human_results = [detection for detection in result.detections if detection.categories[0].category_name == 'person']
        
        if human_results:
            result.detections = human_results
            detection_result_list.append(result)

        if human_results:
            print(f"Kết quả nhận diện (FPS: {FPS:.1f}):")
            for detection in human_results:
                bbox = detection.bounding_box
                print(f" - Người: tọa độ x={bbox.origin_x}, y={bbox.origin_y}, "
                      f"rộng={bbox.width}, cao={bbox.height}")

        COUNTER += 1

    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           running_mode=vision.RunningMode.LIVE_STREAM,
                                           max_results=max_results, score_threshold=score_threshold,
                                           result_callback=save_result)
    detector = vision.ObjectDetector.create_from_options(options)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit('ERROR: Không thể đọc từ webcam. Vui lòng kiểm tra cấu hình webcam.')

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        if cv2.waitKey(1) == 27:
            break

    detector.close()
    cap.release()

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
