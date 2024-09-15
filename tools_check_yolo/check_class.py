#quả code này để test xem trong cái trọng số .pt có các lớp nào và nằm ở vị trí bao nhiêu

from ultralytics import YOLO

# Tải mô hình YOLO
model = YOLO("yolov5n.pt")

# Lấy tên các lớp từ mô hình
classes = model.names

# In danh sách các lớp để kiểm tra chỉ số của lớp `person`
print(classes)