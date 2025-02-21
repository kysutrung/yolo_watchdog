import tkinter as tk
from tkinter import Label, Button, Toplevel, Listbox, MULTIPLE, Scrollbar
from PIL import Image, ImageTk
import threading
import cv2
from ultralytics import YOLO
import numpy as np
import struct
import serial

#==========SETTING==========================================================
model = YOLO("yolov8n.pt")  #trọng số
hinh_anh_dau_vao = cv2.VideoCapture(0)  #camera
ser = serial.Serial('COM5', 115200, timeout=1)  #cổng cắm bộ phát tín hiệu
#===========================================================================

cac_doi_tuong_cam = ["bottle", "person", "cell phone", "knife"] #đối tượng cấm
cai_dat_khu_vuc = [[] for _ in range(9)] #lưu cài đặt của 8 khu vực


def xac_dinh_vi_tri_vat_the(x_center, y_center):
    if x_center < 160 and y_center < 240:
        return 1
    elif x_center > 160 and x_center < 320 and y_center < 240:
        return 2
    elif x_center > 320 and x_center < 480 and y_center < 240:
        return 3
    elif x_center > 480 and x_center < 640 and y_center < 240:
        return 4
    elif x_center < 160 and y_center > 240:
        return 5
    elif x_center > 160 and x_center < 320 and y_center > 240:
        return 6
    elif x_center > 320 and x_center < 480 and y_center > 240:
        return 7
    elif x_center > 480 and x_center < 640 and y_center > 240:
        return 8

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 2.0")
        self.geometry("400x400")

        #logo
        self.logo_label = Label(self)
        self.logo_label.pack(pady=10)
        try:
            image = Image.open("app_logo.png")
            image = image.resize((380, 120))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)")

        self.label_chu_thich = Label(self, text="Settings", font=("Arial", 12, "bold"))
        self.label_chu_thich.pack(pady=(10, 5))

        #khung chứa các nút khu vực cho ngay ngắn đẹp
        self.frame_khu_vuc = tk.Frame(self)
        self.frame_khu_vuc.pack(pady=10)

        #8 nút khu vực
        self.cac_nut_khu_vuc = []
        for i in range(1, 9):
            button = Button(self.frame_khu_vuc, text=f"Area {i}", command=lambda k=i: self.mo_cua_so_lua_chon(k))
            button.grid(row=(i-1)//4, column=(i-1)%4, padx=5, pady=5)  
            self.cac_nut_khu_vuc.append(button)

        #nút nhấn START/STOP
        self.button = Button(self, text="START / STOP", font=("Arial", 10, "bold"), command=self.on_click)
        self.button.pack(pady=(20,10))
        self.label = Label(self, text="Stopped")
        self.label.pack()

        self.video_window = None

    #nút start + stop
    def on_click(self):
        self.running = not self.running
        self.label.config(text="Running" if self.running else "Stopped")

        if self.running:
            self.video_window = Toplevel(self)
            self.video_window.title("Realtime Video")
            self.video_label = Label(self.video_window)
            self.video_label.pack()
            self.thread = threading.Thread(target=self.yolo_watchdog, daemon=True)
            self.thread.start()
        else:
            if self.video_window:
                self.video_window.destroy()
                self.video_window = None
    
    #cửa sổ lựa chọn đối tượng
    def mo_cua_so_lua_chon(self, khu_vuc):
        cua_so_lua_chon = Toplevel(self)
        cua_so_lua_chon.title(f"Banned Objects In Area {khu_vuc}")
        cua_so_lua_chon.geometry("350x400")
        
        #scrollbar
        scrollbar = Scrollbar(cua_so_lua_chon)
        scrollbar.pack(side="right", fill="y")

        #listbox
        listbox = Listbox(cua_so_lua_chon, selectmode=MULTIPLE)
        for item in cac_doi_tuong_cam:
            listbox.insert(tk.END, item)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)
        
        #cấu hình scrollbar
        scrollbar.config(command=listbox.yview)

        def xac_nhan_lua_chon():
            cai_dat_khu_vuc[khu_vuc].extend(cac_doi_tuong_cam[i] for i in listbox.curselection())
            cua_so_lua_chon.destroy()

        #nút xác nhận
        button_xac_nhan = Button(cua_so_lua_chon, text="CONFIRM", command=xac_nhan_lua_chon)
        button_xac_nhan.pack(pady=10)

    def yolo_watchdog(self):
        while self.running:
            #bắt đầu thu thập hình ảnh
            doc_thanh_cong, khung_hinh = hinh_anh_dau_vao.read()
            if not doc_thanh_cong:
                break
            
            #khởi tạo nhận diện hình ảnh
            ket_qua = model.predict(source=khung_hinh,
                                    conf=0.3, 
                                    device="cuda", 
                                    classes=[39, 43, 67, 0], 
                                    show=False)
            
            #đoạn này phân tích kết quả nhận diện
            for vat_the in ket_qua:
                numbers = [0] * 8

                for box in vat_the.boxes:
                    id_vat_the = int(box.cls.cpu().numpy())  
                    ten_vat_the = vat_the.names[id_vat_the]  
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x_tam = int((x1 + x2) / 2)
                    y_tam = int((y1 + y2) / 2)
                    khu_vuc_vi_pham = xac_dinh_vi_tri_vat_the(x_tam, y_tam)
                    print("Phát hiện vi phạm tại khu vực: " + str(khu_vuc_vi_pham))
                    if khu_vuc_vi_pham is not None:
                        if ten_vat_the in cai_dat_khu_vuc[khu_vuc_vi_pham]:
                            numbers[khu_vuc_vi_pham - 1] += 1
                            
                        
                
                #gửi kết quả nhận diện qua bộ phát sóng
                data = struct.pack('8i', *numbers)
                ser.write(data)
                print("Đã gửi dữ liệu:", numbers)

            #đoạn này vẽ lưới ô và đánh số ô
            h, w, _ = khung_hinh.shape
            for i in range(1, 4):
                cv2.line(khung_hinh, (w * i // 4, 0), (w * i // 4, h), (0, 255, 0), 2)
            for i in range(1, 2):
                cv2.line(khung_hinh, (0, h * i // 2), (w, h * i // 2), (0, 255, 0), 2)

            for i in range(4):
                for j in range(2):
                    cv2.putText(khung_hinh, str(i + j * 4 + 1), (w * i // 4 + 10, h * j // 2 + 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            #hiển thị hình ảnh realtime
            khung_hinh = cv2.cvtColor(khung_hinh, cv2.COLOR_BGR2RGB)
            khung_hinh = Image.fromarray(khung_hinh)
            khung_hinh = ImageTk.PhotoImage(image=khung_hinh)

            self.video_label.config(image=khung_hinh)
            self.video_label.image = khung_hinh

            if not self.running:
                break
        
        hinh_anh_dau_vao.release()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
