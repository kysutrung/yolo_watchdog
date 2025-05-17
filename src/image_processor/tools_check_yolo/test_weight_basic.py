from ultralytics import YOLO

import cv2

model = YOLO("for_image_processor/yolo_weight/yolov8n.pt")

results = model.predict(source="1", 
                        conf=0.3,
                        device="cuda",
                        classes=[0],
                        show=True)