import cv2
from ultralytics import YOLO
import numpy as np

Black = (0, 0, 0)
Red = (255, 0, 0)
Leon = (0, 255, 0)

def chia_khung(hang, cot):
    
    model = YOLO('yolov8_custom.pt')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("khong the truy cap camera")
        return

    while True:
        print("dm code1")
        #doc tu khung hinh webcam
        ret, frame = cap.read()
        if not ret:
            print("khong the doc khung hinh tu khung")
            break
        print("dm code2")
        
        #nhan dien vat the
        results = model(frame)
        
        height, width, _ = frame.shape
        
        rows = hang
        cols = cot
        
        height_cell = height // rows
        width_cell = width // cols
        
        #ve luoi chia anh -> toa do
        for i in range(cols):
            for j in range(rows):
                x_start = i*width_cell
                x_end = (i+1)*width_cell
                y_start = j*height_cell
                y_end = (j+1)*height_cell
                #ve o
                cv2.rectangle(frame, (int(x_start), int(y_start)), (int(x_end), int(y_end)), Red, 1)
                cv2.putText(frame, f'({i},{j})', (x_start + 5, y_start + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, Black,1)
        
        #lay ket qua nhan dien
        #boxes = results[0].boxes.xyxy.cpu().numpy() #bounding boxes voi dinh dang [x1, y1, x2, y2, confidence, class]
        #for box in boxes:
            #x1, y1, x2, y2, confidence, class_id = box
            #w = x2 -x1
            #h = y2 - y1
                
            #ve bounding box
            #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), Leon, 2)
            #cv2.putText(frame, f"ID: {int(class_id)} Conf: {confidence:.2f}", (int(x1),int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, Leon, 2)
            
            #print(f"Bounding Box: {int(x1)}, y1={int(y1)}, width={int(w)}, height={int(h)}")
            
        #Hien thi khung hinh       
        cv2.imshow('Webcam', frame)
        

a = 4
b = 4
chia_khung(a,b)