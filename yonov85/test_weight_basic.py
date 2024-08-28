from ultralytics import YOLO

import cv2

model = YOLO("yolov8_cust2.pt")

results = model.predict(source="0", 
                        conf=0.3,
                        device="cuda",
                        classes=[0],
                        show=True)