import tkinter as tk
from tkinter import Label, Button, Toplevel, Listbox, MULTIPLE, Scrollbar
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import cv2
from ultralytics import YOLO
import numpy as np
import struct
import serial
import serial.tools.list_ports
import speech_recognition as sr
from gtts import gTTS
import pygame
import os

#==========SETTING==========================================================
model = YOLO("yolov8n.pt")  # trọng số

#==========GLOBAL_VAR==================================================
cac_doi_tuong_cam = ["bottle", "person", "cell phone"]  # đối tượng cấm
cai_dat_khu_vuc = [[] for _ in range(9)]  # lưu cài đặt của 8 khu vực (index 1..8 dùng)
khu_vuc_co_nguoi = [0 for _ in range(8)]
khu_vuc_co_chai = [0 for _ in range(8)]
khu_vuc_co_dien_thoai = [0 for _ in range(8)]

voice_command_running = False

#==========XỬ LÝ GIỌNG NÓI============================================
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        text_to_speech("Xin mời nói")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="vi-VI")
            print("Nghe được: {}".format(text))
            return text
        except Exception as e:
            print(f"Không nhận dạng được giọng nói! Lỗi: {e}")
            return None

def process_command(text):
    text = text.lower()
    
    tim_nguoi_keywords = ["tìm người", "tìm kiếm người", "phát hiện người", "người ở đâu", "người đâu", "người đâu rồi", "đang có người"]
    tim_chai_keywords = ["tìm chai nước", "tìm kiếm chai nước", "phát hiện chai nước", "chai nước ở đâu", "chai nước đâu", "chai nước đâu rồi", "đang có chai nước"]
    tim_dien_thoai_keywords = ["tìm điện thoại", "tìm kiếm điện thoại", "phát hiện điện thoại", "điện thoại ở đâu", "điện thoại đâu", "điện thoại đâu rồi", "đang có điện thoại"]

    for keyword in tim_nguoi_keywords:
        if keyword in text:
            return tim_nguoi()

    for keyword in tim_chai_keywords:
        if keyword in text:
            return tim_chai()

    for keyword in tim_dien_thoai_keywords:
        if keyword in text:
            return tim_dien_thoai()
    
    return "Lệnh không hợp lệ"

def text_to_speech(text):
    try:
        output = gTTS(text, lang="vi", slow=False)
        filename = "output.mp3"
        output.save(filename)
        
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.quit()
        
        os.remove(filename)
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")

def tim_nguoi():
    string_a = "Không phát hiện người ở bất kỳ khu vực nào"
    khu_vuc_thuc_su_co_nguoi = [str(i+1) for i in range(8) if khu_vuc_co_nguoi[i] > 0]
    
    if any(khu_vuc_co_nguoi):
        string_a = "Phát hiện người ở khu vực " + " ".join(khu_vuc_thuc_su_co_nguoi)
    
    return string_a

def tim_dien_thoai():
    string_a = "Không phát hiện điện thoại ở bất kỳ khu vực nào"
    khu_vuc_thuc_su_co_dien_thoai = [str(i+1) for i in range(8) if khu_vuc_co_dien_thoai[i] > 0]
    
    if any(khu_vuc_co_dien_thoai):
        string_a = "Phát hiện điện thoại ở khu vực " + " ".join(khu_vuc_thuc_su_co_dien_thoai)
    
    return string_a

def tim_chai():
    string_a = "Không phát hiện cái chai ở bất kỳ khu vực nào"
    khu_vuc_thuc_su_co_chai = [str(i+1) for i in range(8) if khu_vuc_co_chai[i] > 0]
    
    if any(khu_vuc_co_chai):
        string_a = "Phát hiện chai ở khu vực " + " ".join(khu_vuc_thuc_su_co_chai)
    
    return string_a

def voice_commandz():
    global voice_command_running
    while voice_command_running:
        text = speech_to_text()
        if text:
            response = process_command(text)
            text_to_speech(response)

#==========XỬ LÝ KHU VỰC=================================================

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
    else:
        return None

#==========GIAO DIỆN CHÍNH VÀ LOGIC=======================================

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 3.0")
        self.geometry("420x650")

        self.hinh_anh_dau_vao = cv2.VideoCapture(0) #Chọn cam ở đây
        if not self.hinh_anh_dau_vao.isOpened():
             print("Không thể mở camera")
             self.running = False
        
        self.thread = None
        self.video_window = None
        self.video_label = None

        # logo
        self.logo_label = Label(self)
        self.logo_label.pack(pady=10)
        try:
            image = Image.open("app_logo.png")
            image = image.resize((380, 150))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)")

        self.label_chu_thich = Label(self, text="Set up restricted areas", font=("Arial", 12, "bold"))
        self.label_chu_thich.pack(pady=(10, 5))

        # khung chứa các nút khu vực
        self.frame_khu_vuc = tk.Frame(self)
        self.frame_khu_vuc.pack(pady=10)

        # 8 nút khu vực
        self.cac_nut_khu_vuc = []
        for i in range(1, 9):
            button = Button(self.frame_khu_vuc, text=f"Area {i}", command=lambda k=i: self.mo_cua_so_lua_chon(k), bg="blue", fg="white")
            button.grid(row=(i-1)//4, column=(i-1)%4, padx=5, pady=5)
            self.cac_nut_khu_vuc.append(button)

        # Nút chọn cổng COM
        self.label_com = Label(self, text="Select COM port", font=("Arial", 12, "bold"))
        self.label_com.pack(pady=(10, 10))

        self.combobox_com = ttk.Combobox(self, state="readonly")
        self.combobox_com.pack(pady=(0, 10))
        self.refresh_com_ports()
        self.combobox_com.bind("<<ComboboxSelected>>", self.on_com_selected)

        self.ser = None 

        # Nút START / STOP
        self.button = Button(self, text="START / STOP", font=("Arial", 10, "bold"), command=self.on_click,
                             width=15, height=2,
                             bg="red", fg="white",
                             padx=10, pady=5)
        self.button.pack(pady=(20, 10))
        self.label = Label(self, text="Stopped")
        self.label.pack()

        # Nút bật tắt giọng nói
        self.voice_button = Button(self, text="VOICE COMMAND", font=("Arial", 10, "bold"), command=self.toggle_voice_command,
                                     width=15, height=2,
                                     bg="white", fg="black",
                                     padx=10, pady=5)
        self.voice_button.pack(pady=(10, 10))
        global voice_command_running
        voice_command_running = False
        self.voice_status_label = Label(self, text="Inactive")
        self.voice_status_label.pack()

        # Khởi tạo cổng COM mặc định
        try:
            self.ser = serial.Serial('COM5', 115200, timeout=1)  # cổng cắm bộ phát tín hiệu
        except serial.SerialException as e:
            print(f"Không thể mở cổng COM5: {e}")
            self.ser = None

        # Đóng camera khi tắt app
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Làm mới danh sách cổng COM
    def refresh_com_ports(self):
        ports = serial.tools.list_ports.comports()
        com_list = [port.device for port in ports]
        if not com_list:
            com_list = ["Không có cổng COM"]
        self.combobox_com['values'] = com_list
        self.combobox_com.current(0)

    # Xử lý khi chọn cổng COM mới
    def on_com_selected(self, event):
        selected_port = self.combobox_com.get()
        self.open_serial(selected_port)

    def open_serial(self, port_name):
        if self.ser and self.ser.is_open:
            self.ser.close()
        try:
            self.ser = serial.Serial(port_name, 115200, timeout=1)
            print(f"Đã kết nối cổng {port_name}")
        except Exception as e:
            print(f"Lỗi khi mở cổng {port_name}: {e}")
            self.ser = None

    # Nút bật tắt giọng nói
    def toggle_voice_command(self):
        global voice_command_running
        voice_command_running = not voice_command_running
        
        if voice_command_running:
            self.voice_status_label.config(text="Active")
            self.voice_thread = threading.Thread(target=voice_commandz, daemon=True)
            self.voice_thread.start()
        else:
            self.voice_status_label.config(text="Inactive")

    # Nút START / STOP
    def on_click(self):
        self.running = not self.running
        self.label.config(text="Running" if self.running else "Stopped")

        if self.running:
            # Mở camera mỗi khi start
            if not self.hinh_anh_dau_vao.isOpened():
                self.hinh_anh_dau_vao = cv2.VideoCapture(0)
                if not self.hinh_anh_dau_vao.isOpened():
                    print("Không thể mở camera")
                    self.running = False
                    self.label.config(text="Stopped")
                    return

            # Tạo cửa sổ video nếu chưa tồn tại
            if self.video_window is None or not self.video_window.winfo_exists():
                self.video_window = Toplevel(self)
                self.video_window.title("Realtime Video")
                self.video_label = Label(self.video_window)
                self.video_label.pack()

            self.thread = threading.Thread(target=self.yolo_watchdog, daemon=True)
            self.thread.start()
        else:
            # Giải phóng camera khi stop
            if self.hinh_anh_dau_vao.isOpened():
                self.hinh_anh_dau_vao.release()

            # Đóng cửa sổ video
            if self.video_window:
                self.video_window.destroy()
                self.video_window = None

    # Cửa sổ lựa chọn đối tượng cấm cho khu vực
    def mo_cua_so_lua_chon(self, khu_vuc):
        cua_so_lua_chon = Toplevel(self)
        cua_so_lua_chon.title(f"Banned Objects In Area {khu_vuc}")
        cua_so_lua_chon.geometry("350x400")

        scrollbar = Scrollbar(cua_so_lua_chon)
        scrollbar.pack(side="right", fill="y")

        listbox = Listbox(cua_so_lua_chon, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        for item in cac_doi_tuong_cam:
            listbox.insert(tk.END, item)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        scrollbar.config(command=listbox.yview)

        def xac_nhan_lua_chon():
            cai_dat_khu_vuc[khu_vuc] = [cac_doi_tuong_cam[i] for i in listbox.curselection()]
            cua_so_lua_chon.destroy()

        button_xac_nhan = Button(cua_so_lua_chon, text="CONFIRM", command=xac_nhan_lua_chon)
        button_xac_nhan.pack(pady=10)

    # Hàm chính xử lý video và nhận diện
    def yolo_watchdog(self):
        while self.running:
            doc_thanh_cong, khung_hinh = self.hinh_anh_dau_vao.read()
            if not doc_thanh_cong:
                print("Không đọc được khung hình từ camera")
                break

            ket_qua = model.predict(source=khung_hinh,
                                    conf=0.3,
                                    device="cuda",
                                    classes=[39, 43, 67, 0],
                                    show=False)
            
            numbers = [0] * 8
            numbers01 = [0] * 8
            numbers02 = [0] * 8
            numbers03 = [0] * 8

            for vat_the in ket_qua:
                for box in vat_the.boxes:
                    id_vat_the = int(box.cls.cpu().numpy())
                    ten_vat_the = vat_the.names[id_vat_the]
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x_tam = int((x1 + x2) / 2)
                    y_tam = int((y1 + y2) / 2)
                    khu_vuc_vi_pham = xac_dinh_vi_tri_vat_the(x_tam, y_tam)

                    if khu_vuc_vi_pham is not None:
                        if ten_vat_the in cai_dat_khu_vuc[khu_vuc_vi_pham]:
                            numbers[khu_vuc_vi_pham - 1] += 1

                        if ten_vat_the == "person":
                            numbers01[khu_vuc_vi_pham - 1] += 1
                        if ten_vat_the == "bottle":
                            numbers02[khu_vuc_vi_pham - 1] += 1
                        if ten_vat_the == "cell phone":
                            numbers03[khu_vuc_vi_pham - 1] += 1

            for i in range(8):
                khu_vuc_co_nguoi[i] = numbers01[i]
                khu_vuc_co_chai[i] = numbers02[i]
                khu_vuc_co_dien_thoai[i] = numbers03[i]

            # Gửi dữ liệu qua cổng serial nếu đã kết nối
            if self.ser and self.ser.is_open:
                data = struct.pack('8i', *numbers)
                self.ser.write(data)
                print("Đã gửi dữ liệu:", numbers)

            print("Phát hiện người ở:", khu_vuc_co_nguoi)
            print("Phát hiện chai ở:", khu_vuc_co_chai)
            print("Phát hiện điện thoại ở:", khu_vuc_co_dien_thoai)
            
            # Vẽ lưới và số khu vực
            h, w, _ = khung_hinh.shape
            for i in range(1, 4):
                cv2.line(khung_hinh, (w * i // 4, 0), (w * i // 4, h), (0, 255, 0), 2)
            for i in range(1, 2):
                cv2.line(khung_hinh, (0, h * i // 2), (w, h * i // 2), (0, 255, 0), 2)

            for i in range(4):
                for j in range(2):
                    cv2.putText(khung_hinh, str(i + j * 4 + 1), (w * i // 4 + 10, h * j // 2 + 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            khung_hinh = cv2.cvtColor(khung_hinh, cv2.COLOR_BGR2RGB)
            khung_hinh = Image.fromarray(khung_hinh)
            khung_hinh = ImageTk.PhotoImage(image=khung_hinh)

            if self.video_label and self.video_label.winfo_exists():
                self.video_label.config(image=khung_hinh)
                self.video_label.image = khung_hinh

    def on_closing(self):
        if self.hinh_anh_dau_vao is not None:
            self.hinh_anh_dau_vao.release()
        self.destroy()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
