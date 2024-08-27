from ultralytics import YOLO
import cv2

# Tải mô hình YOLOv8
model = YOLO(r"C:\Users\trung\Downloads\anomaly_detector\yolov8_custom\yolov8_custom.pt")

# Mở kết nối với webcam (source="0" là webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển ảnh đầu vào sang grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Chuyển ảnh grayscale về lại dạng 3 kênh để tương thích với YOLOv8
    frame_gray_3ch = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)

    # Dự đoán với mô hình YOLOv8
    results = model.predict(source=frame_gray_3ch, show=True)
    
    # Hiển thị kết quả (nếu bạn muốn hiển thị trong cửa sổ riêng)
    # cv2.imshow("YOLOv8", results[0].plot())

    # Thoát vòng lặp nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng bộ nhớ
cap.release()
cv2.destroyAllWindows()

print(results)
