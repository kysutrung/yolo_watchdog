import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk  # Chỉ cần nếu muốn hiển thị ảnh (có sẵn trong Python bản đầy đủ)

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 1.0")
        self.geometry("400x210")

        # Hiển thị logo nếu có
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
        self.button.pack(pady=10)

        # Hiển thị trạng thái
        self.label = Label(self, text="Stopped", font=("Arial", 12))
        self.label.pack()

    def on_click(self):
        self.running = not self.running
        self.label.config(text="Running" if self.running else "Stopped")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
