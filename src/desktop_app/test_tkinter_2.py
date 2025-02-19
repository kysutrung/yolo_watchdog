import tkinter as tk
from tkinter import Label, Button, Toplevel, Checkbutton, IntVar, StringVar, OptionMenu
from PIL import Image, ImageTk
import threading
import cv2
from ultralytics import YOLO
import numpy as np
import struct
import serial
import time

#==========SETTING============================================
model = YOLO("yolov8n.pt")  #trọng số
hinh_anh_dau_vao = cv2.VideoCapture(0)  #camera
ser = serial.Serial('COM10', 115200, timeout=1) #cổng cắm bộ phát tín hiệu
#=============================================================

class SettingsWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cài Đặt")
        self.geometry("350x200")
        
        Label(self, text="Chọn Khu Vực", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
        self.selected_zone = StringVar(self)
        self.selected_zone.set("Chọn")  # Giá trị mặc định
        self.zone_menu = OptionMenu(self, self.selected_zone, "Khu vực 1", "Khu vực 2", "Khu vực 3", "Khu vực 4")
        self.zone_menu.grid(row=0, column=1, padx=10, pady=10)
        
        Label(self, text="Thiết Lập Hạn Chế", font=("Arial", 10, "bold")).grid(row=1, column=1)
        
        self.restrict_bottle = IntVar()
        self.restrict_person = IntVar()
        self.restrict_phone = IntVar()
        
        Checkbutton(self, text="Chai nước", variable=self.restrict_bottle).grid(row=2, column=1, sticky='w')
        Checkbutton(self, text="Người", variable=self.restrict_person).grid(row=3, column=1, sticky='w')
        Checkbutton(self, text="Điện thoại", variable=self.restrict_phone).grid(row=4, column=1, sticky='w')
        
        Button(self, text="Xác nhận", command=self.save_settings).grid(row=5, column=1, pady=10)
        
        self.parent = parent
    
    def save_settings(self):
        self.parent.settings['zone'] = self.selected_zone.get()
        self.parent.settings['restrict_bottle'] = self.restrict_bottle.get()
        self.parent.settings['restrict_person'] = self.restrict_person.get()
        self.parent.settings['restrict_phone'] = self.restrict_phone.get()
        print("Cài đặt lưu: ", self.parent.settings)
        self.destroy()

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 1.0")
        self.geometry("400x250")
        
        self.settings = {  # Lưu cài đặt
            'zone': "",
            'restrict_bottle': 0,
            'restrict_person': 0,
            'restrict_phone': 0
        }
        
        # Logo
        self.logo_label = Label(self)
        self.logo_label.pack()
        try:
            image = Image.open("logo_demo2.png")
            image = image.resize((380, 120))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)")
        
        # Nút nhấn
        self.button = Button(self, text="START / STOP", command=self.on_click)
        self.button.pack(pady=(10, 5))
        self.label = Label(self, text="Stopped", font=("Arial", 12))
        self.label.pack()
        
        # Nút cài đặt
        self.settings_button = Button(self, text="Cài Đặt", command=self.open_settings)
        self.settings_button.pack(pady=5)
        
        self.video_window = None
    
    def open_settings(self):
        SettingsWindow(self)
    
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
            # Bắt đầu thu thập hình ảnh
            doc_thanh_cong, khung_hinh = hinh_anh_dau_vao.read()
            if not doc_thanh_cong:
                break
            
            # Khởi tạo nhận diện hình ảnh
            ket_qua = model.predict(source=khung_hinh, conf=0.3, device="cuda", show=False)
            
            # Kiểm tra cài đặt hạn chế
            restricted_classes = []
            if self.settings['restrict_bottle']:
                restricted_classes.append(39)  # Chai nước
            if self.settings['restrict_person']:
                restricted_classes.append(0)   # Người
            if self.settings['restrict_phone']:
                restricted_classes.append(67)  # Điện thoại
            
            for vat_the in ket_qua:
                for box in vat_the.boxes:
                    id_vat_the = int(box.cls.cpu().numpy())
                    if id_vat_the in restricted_classes:
                        print("Phát hiện vi phạm:", vat_the.names[id_vat_the])
            
            # Hiển thị hình ảnh realtime
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
