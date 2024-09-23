from ultralytics import YOLO
import cv2

model = YOLO("yolov8_cust2.pt")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray_3ch = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)

    results = model.predict(source=frame_gray_3ch, show=True)
    
    cv2.imshow("YOLOv8", results[0].plot())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
