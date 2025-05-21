import tkinter as tk
from threading import Thread
import cv2, serial, time, os, pygame
from ultralytics import YOLO
from datetime import datetime

print("RUNNING...")

model = YOLO("for_image_processor/yolo_weight/yolov8n.pt")
CAM_ID, WIDTH, HEIGHT = 1, 640, 480
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
DEAD_ZONE, STEP = 40, 2
servo1, servo2, auto_tracking, last_alert = 90, 90, False, 0
pygame.mixer.init()
ALERT = "for_image_processor/alert.mp3"
LOG_FILE = "for_image_processor/detections_log.txt"

try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    def send_servo(i, a):
        ser.write(f"{i}:{max(0, min(180, a))}\n".encode())
    send_servo(1, servo1)
    send_servo(2, servo2)
except:
    ser = None
    def send_servo(i, a): pass

def play_alert():
    if os.path.exists(ALERT):
        try: pygame.mixer.Sound(ALERT).play()
        except: pass

def log_detection():
    with open(LOG_FILE, "a") as f:
        f.write(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] Phat hien nguoi \n"))

def video_loop():
    global servo1, servo2, auto_tracking, last_alert
    cap = cv2.VideoCapture(CAM_ID)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        results = model.predict(frame, conf=0.3, device='cuda', classes=[0], verbose=False)
        boxes = results[0].boxes

        if boxes:
            if time.time() - last_alert > 5:
                play_alert()
                log_detection()
                last_alert = time.time()

            box = max(boxes, key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1]))
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
            cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (255,0,0), -1)

            if auto_tracking:
                if abs(cx - CENTER_X) > DEAD_ZONE:
                    servo1 += STEP if cx < CENTER_X else -STEP
                    send_servo(1, servo1)
                    servo1_scale.set(servo1)  
                if abs(cy - CENTER_Y) > DEAD_ZONE:
                    servo2 += STEP if cy < CENTER_Y else -STEP
                    send_servo(2, servo2)
                    servo2_scale.set(servo2)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == 27: break

    cap.release()
    cv2.destroyAllWindows()

def toggle_tracking():
    global auto_tracking
    auto_tracking = not auto_tracking
    status.config(text=f"Auto Tracking: {'ON' if auto_tracking else 'OFF'}")
    button.config(text="Tắt" if auto_tracking else "Bật")

def update_servo1(val):
    global servo1
    servo1 = int(val)
    if not auto_tracking:
        send_servo(1, servo1)

def update_servo2(val):
    global servo2
    servo2 = int(val)
    if not auto_tracking:
        send_servo(2, servo2)

#Giao diện
root = tk.Tk()
root.title("YOLO WatchDog Tracker")
root.geometry("300x350")

status = tk.Label(root, text="Auto Tracking: OFF", font=("Arial", 16, "bold"))
status.pack(pady=10)

button = tk.Button(root, text="Bật", font=("Arial", 14), bg='red', fg='white', command=toggle_tracking)
button.pack(pady=10)

manual_control_label = tk.Label(root, text="Manual Control", font=("Arial", 16, "bold"))
manual_control_label.pack(pady=10)

servo1_label = tk.Label(root, text="Right              Left")
servo1_label.pack()
servo1_scale = tk.Scale(root, from_=0, to=180, orient="horizontal", command=update_servo1)
servo1_scale.set(servo1)
servo1_scale.pack(pady=5)

servo2_label = tk.Label(root, text="Down                 Up")
servo2_label.pack()
servo2_scale = tk.Scale(root, from_=0, to=180, orient="horizontal", command=update_servo2)
servo2_scale.set(servo2)
servo2_scale.pack(pady=5)

Thread(target=video_loop, daemon=True).start()
root.mainloop()
