import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import time
from ultralytics import YOLO
import cv2
import serial
import struct

#==========SETTING============================================
model = YOLO("yolov8n.pt") #thay trọng số ở đây
hinh_anh_dau_vao = cv2.VideoCapture(0) #thay đổi camera ở đây
SERIAL_PORT = "COM10"  #thay đổi cổng cắm bộ phát sóng ở đây
#=============================================================

BAUD_RATE = 115200

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 1.0")
        self.geometry("400x220")

        #hiển thị logo ở đây
        self.logo_label = Label(self)
        self.logo_label.pack()
        try:
            image = Image.open("logo_demo2.png")
            image = image.resize((380, 120))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)")

        #nút nhấn ở đây
        self.button = Button(self, text="START / STOP", command=self.on_click)
        self.button.pack(pady=(20,10))
        self.label = Label(self, text="Stopped", font=("Arial", 12))
        self.label.pack()

    def on_click(self):
        self.running = not self.running
        self.label.config(text="Running" if self.running else "Stopped")

        if self.running:
            #hàm này sẽ chạy trong một luồng riêng
            self.thread = threading.Thread(target=self.yolo_watchdog, daemon=True)
            self.thread.start()

    def yolo_watchdog(self):
        while True:
            doc_thanh_cong, khung_hinh = hinh_anh_dau_vao.read()
            if not doc_thanh_cong:
                break

            ket_qua = model.predict(source=khung_hinh,
                                    conf=0.3,
                                    device="cuda",
                                    classes=[0],
                                    show=True)

            for vat_the in ket_qua:
                for box in vat_the.boxes:
                    id_vat_the = int(box.cls.cpu().numpy())  #ID lớp
                    ten_vat_the = vat_the.names[id_vat_the]  #tên lớp từ danh sách tên lớp
                    #đoạn này tính tọa độ tâm
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x_tam = int((x1 + x2) / 2)
                    y_tam = int((y1 + y2) / 2)
                    print("Phat hien " + ten_vat_the + " tai vi tri: " + str(x_tam) + " " + str(y_tam))

            del ket_qua

            if not self.running: 
                break

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
