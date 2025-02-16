import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import time
from ultralytics import YOLO
import cv2
import serial

model = YOLO("yolov8n.pt") #thay trọng số ở đây

def xac_dinh_vi_tri(x_center, frame_width):
    if 0 <= x_center < frame_width / 4:
        return 4
    elif frame_width / 4 <= x_center < frame_width / 2:
        return 3
    elif frame_width / 2 <= x_center < 3 * frame_width / 4:
        return 2
    elif 3 * frame_width / 4 <= x_center <= frame_width:
        return 1

def tao_mang_ket_qua(num_g, list_b):
    list_b[num_g-1] += 1

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
                                    device="cpu",
                                    classes=[0],
                                    show=False)

            for vat_the in ket_qua:
                #cái mảng này để lưu vị trí
                list_a = [0, 0, 0, 0]
                #cái này tính tọa độ tâm để xem ô nào có người và có bao nhiêu
                for box in vat_the.boxes:
                    #đoạn này tính tọa độ tâm
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x_tam = int((x1 + x2) / 2)
                    y_tam = int((y1 + y2) / 2)

                    #đoạn báo xem vật thể đang ở ô nào
                    tao_mang_ket_qua(xac_dinh_vi_tri(x_tam, 640), list_a)

                data = struct.pack('4i', *list_a)
                ser.write(data)
                print(f"Sent: {list_a}")



if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
