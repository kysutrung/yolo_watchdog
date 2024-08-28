from ultralytics import YOLO

# Tải mô hình YOLOv8 pre-trained
model = YOLO("yolov5n_custom2.pt")

# Lấy tên các lớp từ mô hình
classes = model.names

# In danh sách các lớp để kiểm tra chỉ số của lớp `person`
print(classes)