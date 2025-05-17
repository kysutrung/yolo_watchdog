import tkinter as tk
from threading import Thread
import cv2
import serial
from ultralytics import YOLO
import pygame
import time
import os

# ⚙️ Cài đặt YOLO
model = YOLO("for_image_processor/yolo_weight/yolov8n.pt")

CAM_ID = 1
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CENTER_X = FRAME_WIDTH // 2
CENTER_Y = FRAME_HEIGHT // 2
DEAD_ZONE = 40
STEP = 2

# Servo điều khiển
servo1_angle = 90
servo2_angle = 90
auto_tracking = False
last_alert_time = 0

# 🔊 Âm thanh cảnh báo
ALERT_SOUND_PATH = "alert.mp3"
pygame.mixer.init()

def play_alert():
    if os.path.exists(ALERT_SOUND_PATH):
        try:
            sound = pygame.mixer.Sound(ALERT_SOUND_PATH)
            sound.play()
        except Exception as e:
            print("⚠️ Lỗi phát âm thanh:", e)
    else:
        print("⚠️ File âm thanh không tồn tại:", ALERT_SOUND_PATH)

# Kết nối Serial
try:
    ser = serial.Serial('COM21', 9600, timeout=1)

    def send_servo(servo_id, angle):
        angle = max(0, min(180, angle))
        cmd = f"{servo_id}:{angle}\n"
        if ser and ser.is_open:
            ser.write(cmd.encode())

    send_servo(1, 90)
    send_servo(2, 90)

except Exception as e:
    print("Không thể mở cổng serial:", e)
    ser = None

    def send_servo(servo_id, angle):
        pass

def video_loop():
    global servo1_angle, servo2_angle, auto_tracking, last_alert_time

    cap = cv2.VideoCapture(CAM_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.3, device='cuda', classes=[0], verbose=False)
        boxes = results[0].boxes

        if boxes is not None and len(boxes) > 0:
            current_time = time.time()
            if current_time - last_alert_time > 5:
                play_alert()
                last_alert_time = current_time

            largest_box = max(boxes, key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1]))
            x1, y1, x2, y2 = map(int, largest_box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (255, 0, 0), -1)

            if auto_tracking:
                dx = cx - CENTER_X
                dy = cy - CENTER_Y

                if abs(dx) > DEAD_ZONE:
                    if dx > 0:
                        servo1_angle -= STEP
                    else:
                        servo1_angle += STEP
                    send_servo(1, servo1_angle)

                if abs(dy) > DEAD_ZONE:
                    if dy > 0:
                        servo2_angle -= STEP
                    else:
                        servo2_angle += STEP
                    send_servo(2, servo2_angle)

        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def toggle_tracking():
    global auto_tracking
    auto_tracking = not auto_tracking
    status_label.config(text=f"Auto Tracking: {'ON' if auto_tracking else 'OFF'}")
    toggle_button.config(text="Tắt" if auto_tracking else "Bật")

# Giao diện Tkinter
root = tk.Tk()
root.title("YOLO WatchDog Tracker")
root.geometry("300x150")

status_label = tk.Label(root, text="Auto Tracking: OFF", font=("Arial", 16))
status_label.pack(pady=10)

toggle_button = tk.Button(
    root,
    text="Bật",
    font=("Arial", 14),
    command=toggle_tracking,
    bg='red',
    fg='white'
)
toggle_button.pack(pady=10)

# Chạy video trong luồng riêng
thread = Thread(target=video_loop, daemon=True)
thread.start()

root.mainloop()
