import cv2
import serial
from ultralytics import YOLO

# ⚙️ Cài đặt
model = YOLO("for_image_processor/yolo_weight/yolov8n.pt")

CAM_ID = 1  # Camera ID (0 = webcam, 1 = USB cam)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CENTER_X = FRAME_WIDTH // 2
CENTER_Y = FRAME_HEIGHT // 2
DEAD_ZONE = 40  # Vùng không cần điều chỉnh nếu lệch nhỏ hơn

# Servo điều khiển
servo1_angle = 90  # quay trái/phải (x)
servo2_angle = 90  # ngẩng lên/xuống (y)
STEP = 2

# Serial ESP32
try:
    ser = serial.Serial('COM21', 9600, timeout=1)
except Exception as e:
    print("Không thể mở cổng serial:", e)
    ser = None

def send_servo(servo_id, angle):
    angle = max(0, min(180, angle))  # giới hạn góc
    cmd = f"{servo_id}:{angle}\n"
    if ser and ser.is_open:
        ser.write(cmd.encode())

# Mở camera
cap = cv2.VideoCapture(CAM_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Phát hiện người
    results = model.predict(source=frame, conf=0.3, device='cuda', classes=[0], verbose=False)
    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:
        # Chọn bounding box lớn nhất (người gần nhất)
        largest_box = max(boxes, key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1]))
        x1, y1, x2, y2 = map(int, largest_box.xyxy[0])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Vẽ khung và tâm
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (255, 0, 0), -1)

        # So sánh và điều chỉnh
        dx = cx - CENTER_X
        dy = cy - CENTER_Y

        if abs(dx) > DEAD_ZONE:
            if dx > 0:
                servo1_angle -= STEP  # Người lệch phải → quay phải (giảm góc)
            else:
                servo1_angle += STEP  # Người lệch trái → quay trái (tăng góc)
            send_servo(1, servo1_angle)

        if abs(dy) > DEAD_ZONE:
            if dy > 0:
                servo2_angle -= STEP  # Người thấp → cúi xuống
            else:
                servo2_angle += STEP  # Người cao → ngẩng lên
            send_servo(2, servo2_angle)

    # Hiển thị
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
