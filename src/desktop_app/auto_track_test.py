from ultralytics import YOLO
import cv2
import serial
import time

# Tải mô hình YOLO
model = YOLO("for_image_processor/yolo_weight/yolov8n.pt")

# Kết nối với ESP32 qua cổng USB (COM port, ví dụ 'COM3' trên Windows hoặc '/dev/ttyUSB0' trên Linux)
ser = serial.Serial('COM19', 115200)  # Thay 'COM3' bằng cổng USB thực tế của bạn
time.sleep(2)  # Đợi 2 giây để ESP32 có thể khởi động và nhận tín hiệu

# Bắt nguồn từ webcam
cap = cv2.VideoCapture(1)

while True:
    # Đọc một khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Dự đoán đối tượng trong khung hình
    results = model.predict(source=frame, conf=0.3, device="cpu", classes=[0], show=False)

    # Lấy bounding boxes và gửi tọa độ tâm qua cổng USB
    for result in results:
        # Lấy các bounding box (x1, y1, x2, y2)
        boxes = result.boxes.xyxy.cpu().numpy()

        for box in boxes:
            # Lấy tọa độ của bounding box
            x1, y1, x2, y2 = box
            # Tính toán tọa độ tâm và làm tròn
            center_x = round((x1 + x2) / 2)
            center_y = round((y1 + y2) / 2)
            print(f"Bounding box center: ({center_x}, {center_y})")

            # Gửi tọa độ tâm qua cổng USB đến ESP32
            ser.write(f"{center_x},{center_y}\n".encode())

            # Vẽ bounding box và tâm lên ảnh
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

    # Hiển thị khung hình với bounding boxes
    cv2.imshow("Frame", frame)

    # Dừng khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
