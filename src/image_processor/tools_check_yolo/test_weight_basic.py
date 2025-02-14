from ultralytics import YOLO

import cv2

model = YOLO("yolov8n.pt")

results = model.predict(source="0", 
                        conf=0.3,
                        device="cpu",
                        classes=[0],
                        show=True)