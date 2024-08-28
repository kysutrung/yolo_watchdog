from ultralytics import YOLO

model = YOLO("yolov8_cust2.pt")
    
results = model.predict(source="0", show=True)

print(results)