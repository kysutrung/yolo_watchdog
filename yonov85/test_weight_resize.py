from ultralytics import YOLO
import cv2
import numpy as np

def degrade_image(image, num_a):
    width = int(image.shape[1] * num_a)
    height = int(image.shape[0] * num_a)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image
 
model = YOLO("yolov8_cust2.pt")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    num_c = 0.5
    degraded_frame = degrade_image(frame,num_c)

    results = model.predict(
        source=degraded_frame,
        conf=0.3,
        device="cpu",
        classes=[0, 1, 2, 3],
        show=True
    )
