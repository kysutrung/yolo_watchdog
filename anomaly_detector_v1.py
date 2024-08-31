import serial
import time
import struct

from ultralytics import YOLO
import cv2

# Cấu hình cổng serial
ser = serial.Serial('/dev/ttyUSB0', 115200) #check lại khi kết nối cam
time.sleep(2)  # Đợi Arduino khởi động


# Cấu hình mô hình Yolo
model = YOLO("yolov8n.pt")
hinh_anh_dau_vao = cv2.VideoCapture(0)

def xac_dinh_vi_tri(x_center, frame_width):
    if 0 <= x_center < frame_width / 4:
        return 4
    elif frame_width / 4 <= x_center < frame_width / 2:
        return 3
    elif frame_width / 2 <= x_center < 3 * frame_width / 4:
        return 2
    elif 3 * frame_width / 4 <= x_center <= frame_width:
        return 1
    
def mang_ket_qua(num_g, list_b):
    list_b[num_g-1] += 1


while True:

    doc_thanh_cong, khung_hinh = hinh_anh_dau_vao.read()
    if not doc_thanh_cong:
        break

    ket_qua = model.predict(source=khung_hinh,
                            conf=0.3,
                            device="cpu",
                            classes=[0])

    for vat_the in ket_qua:
        #cái mảng này để lưu vị trí
        list_a = [0, 0, 0, 0]
        #cái này tính tọa độ tâm để xem ô nào có người và có bao nhiêu
        for box in vat_the.boxes:
            #đoạn này tính tọa độ tâm
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x_tam = int((x1 + x2) / 2)
            y_tam = int((y1 + y2) / 2)

            #chia màn hình ra làm 4 ô bằng nhau từ trái qua phải
            #đoạn báo xem vật thể đang ở ô nào
            #print(f"Phát hiện vật thể tại: ({x_tam}, {y_tam})")
            mang_ket_qua(xac_dinh_vi_tri(x_tam, 640), list_a)

        a = list_a[1]
        b = list_a[2]
        c = list_a[3]
        d = list_a[4]
        data = struct.pack('iiii', a, b, c, d)
        ser.write(data)
        ser.flush()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hinh_anh_dau_vao.release()
cv2.destroyAllWindows()
