from ultralytics import YOLO

# Tải mô hình YOLOv8 pre-trained
model = YOLO("yolov8n.pt")

# Lấy tên các lớp từ mô hình
classes = model.names

# In danh sách các lớp để kiểm tra chỉ số của lớp `person`
print(classes)