import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import time
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt") #thay trọng số ở đây

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
        cap = cv2.VideoCapture(0)  
        while self.running: 
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(frame,
                                    conf=0.3,
                                    device="cuda",
                                    classes=[0],
                                    show=False)
            del results
            frame = None #không thấy hiệu quả cho lắm

            if not self.running: 
                break

        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
