from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

def xac_dinh_vi_tri(x_center, frame_width):
    if 0 <= x_center < frame_width / 4:
        print(f"Vật thể đang ở khu 1")
    elif frame_width / 4 <= x_center < frame_width / 2:
        print(f"Vật thể đang ở khu 2")
    elif frame_width / 2 <= x_center < 3 * frame_width / 4:
        print(f"Vật thể đang ở khu 3")
    elif 3 * frame_width / 4 <= x_center <= frame_width:
        print(f"Vật thể đang ở khu 4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame,
                            conf=0.3,
                            device="cpu",
                            classes=[0])

    for result in results:
        for box in result.boxes:
            # Đoạn này tính tọa độ tâm
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Chia màn hình ra làm 4 ô bằng nhau từ trái qua phải
            # Đoạn báo xem vật thể đang ở ô nào
            print(f"Phát hiện vật thể tại: ({center_x}, {center_y})")
            xac_dinh_vi_tri(center_x, 640)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
