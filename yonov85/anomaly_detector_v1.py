from ultralytics import YOLO
import cv2

model = YOLO("yolov8_cust2.pt")
hinh_anh_dau_vao = cv2.VideoCapture(0)

def xac_dinh_vi_tri(x_center, frame_width):
    if 0 <= x_center < frame_width / 4:
        print(f"Vật thể đang ở khu 1")
    elif frame_width / 4 <= x_center < frame_width / 2:
        print(f"Vật thể đang ở khu 2")
    elif frame_width / 2 <= x_center < 3 * frame_width / 4:
        print(f"Vật thể đang ở khu 3")
    elif 3 * frame_width / 4 <= x_center <= frame_width:
        print(f"Vật thể đang ở khu 4")

def giao_tiep_man_hinh():
    print()

while True:
    doc_thanh_cong, khung_hinh = hinh_anh_dau_vao.read()
    if not doc_thanh_cong:
        break

    ket_qua = model.predict(source=khung_hinh,
                            conf=0.3,
                            device="cpu",
                            classes=[1])

    for vat_the in ket_qua:
        for box in vat_the.boxes:
            # Đoạn này tính tọa độ tâm
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x_tam = int((x1 + x2) / 2)
            y_tam = int((y1 + y2) / 2)

            # Chia màn hình ra làm 4 ô bằng nhau từ trái qua phải
            # Đoạn báo xem vật thể đang ở ô nào
            print(f"Phát hiện vật thể tại: ({x_tam}, {y_tam})")
            xac_dinh_vi_tri(x_tam, 640)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hinh_anh_dau_vao.release()
cv2.destroyAllWindows()
