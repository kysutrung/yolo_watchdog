#code convert label voc sang yolo

import os
import xml.etree.ElementTree as ET

# Đường dẫn tới thư mục chứa các file XML (annotations Pascal VOC)
xml_folder = 'C:\\Users\\trung\\Downloads\\anomaly_detector\\data_set\\voc_voc'
# Đường dẫn tới thư mục chứa các file TXT (sẽ chứa annotations theo định dạng YOLO)
output_folder = 'C:\\Users\\trung\\Downloads\\anomaly_detector\\data_set\\yono'

# Tạo thư mục output nếu chưa có
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Danh sách các lớp (labels) trong dataset của bạn
classes = ["box_a", "box_b", "box_c", "man_a"]  # Thay thế bằng danh sách các class của bạn

def convert_voc_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    with open(os.path.join(output_folder, os.path.splitext(os.path.basename(xml_file))[0] + ".txt"), 'w') as f_out:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in classes:
                continue
            class_id = classes.index(class_name)

            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # Tính toán tọa độ trung tâm và kích thước của bounding box theo tỉ lệ ảnh
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / float(image_width)
            height = (ymax - ymin) / float(image_height)

            # Ghi thông tin vào file TXT theo định dạng YOLO
            f_out.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

# Lặp qua tất cả các file XML trong thư mục và chuyển đổi
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith('.xml'):
        convert_voc_to_yolo(os.path.join(xml_folder, xml_file))

print("OK")
