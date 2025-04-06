import cv2
import time
from ultralytics import YOLO

# Tải mô hình YOLO
model = YOLO("yolov8n.pt")

# Mở camera (source=0 là webcam mặc định)
cap = cv2.VideoCapture(0)

# Kiểm tra camera có mở được không
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

# Cấu hình tham số dự đoán
CONFIDENCE = 0.3
CLASSES = [0]  # Chỉ phát hiện người

# Biến đếm
frame_count = 0
start_time = time.time()
duration = 60  # thời gian chạy: 60 giây

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Dự đoán khung hình
    results = model.predict(frame, conf=CONFIDENCE, device="cpu", classes=CLASSES, verbose=False)

    # Hiển thị kết quả
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    frame_count += 1

    # Kiểm tra thời gian đã hết chưa
    if time.time() - start_time > duration:
        break

    # Nhấn 'q' để thoát sớm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()

# Hiển thị kết quả
elapsed_time = time.time() - start_time
fps = frame_count / elapsed_time
print(f"Đã xử lý {frame_count} khung hình trong {elapsed_time:.2f} giây.")
print(f"Tốc độ trung bình: {fps:.2f} FPS.")
