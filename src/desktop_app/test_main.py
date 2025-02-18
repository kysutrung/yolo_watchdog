import tkinter as tk
from tkinter import Label, Button, Toplevel
from PIL import Image, ImageTk
import threading
import cv2
from ultralytics import YOLO
import numpy as np

#==========SETTING============================================
model = YOLO("yolov8n.pt")  #trọng số
hinh_anh_dau_vao = cv2.VideoCapture(0)  #camera
#=============================================================

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 1.0")
        self.geometry("400x220")

        #logo
        self.logo_label = Label(self)
        self.logo_label.pack()
        try:
            image = Image.open("logo_demo2.png")
            image = image.resize((380, 120))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)")

        #nút nhấn
        self.button = Button(self, text="START / STOP", command=self.on_click)
        self.button.pack(pady=(20,10))
        self.label = Label(self, text="Stopped", font=("Arial", 12))
        self.label.pack()
        
        self.video_window = None

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
                                    classes=[39], 
                                    show=False)
            
            #đoạn này phân tích kết quả nhận diện
            for vat_the in ket_qua:
                for box in vat_the.boxes:
                    #xác định tên đối tượng nhận diện được
                    id_vat_the = int(box.cls.cpu().numpy())  #ID lớp
                    ten_vat_the = vat_the.names[id_vat_the]  #tên lớp từ danh sách tên lớp
                    #tính tọa độ tâm
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x_tam = int((x1 + x2) / 2)
                    y_tam = int((y1 + y2) / 2)

                    print("Phat hien " + ten_vat_the + " tai vi tri: " + str(x_tam) + " " + str(y_tam))

            #đoạn này vẽ lưới 8 ô
            h, w, _ = khung_hinh.shape
            for i in range(1, 4):
                cv2.line(khung_hinh, (w * i // 4, 0), (w * i // 4, h), (0, 255, 0), 2)
            for i in range(1, 2):
                cv2.line(khung_hinh, (0, h * i // 2), (w, h * i // 2), (0, 255, 0), 2)
            
            #đoạn này đánh số ô
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
