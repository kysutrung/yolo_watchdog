import cv2
from ultralytics import YOLO
import numpy as np

def chia_khung():
    
    model = YOLO('yolov8_custom.pt')

    cap = cv2.VideoCapture(0)

    while True:
        #doc tu khung hinh webcam
        ret, frame = cap.read()
        if not ret:
            print("khong the doc khung hinh tu khung")
            break
        
        #nhan dien vat the
        results = model(frame)