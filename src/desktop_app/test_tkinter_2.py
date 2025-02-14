import tkinter as tk
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.title("YOLO WatchDog Beta 1.0")
        self.geometry("400x250")
        self.configure(bg="#2c3e50")  # Màu nền tối sang trọng

        # Khung chứa logo
        logo_frame = Frame(self, bg="#2c3e50")
        logo_frame.pack(pady=10)

        # Hiển thị logo nếu có
        self.logo_label = Label(logo_frame, bg="#2c3e50")
        self.logo_label.pack()
        try:
            image = Image.open("logo_demo.png")
            image = image.resize((380, 120))
            self.logo = ImageTk.PhotoImage(image)
            self.logo_label.config(image=self.logo)
        except:
            self.logo_label.config(text="(No Logo)", fg="white", font=("Arial", 12, "bold"))

        # Khung chứa nút và trạng thái
        control_frame = Frame(self, bg="#2c3e50")
        control_frame.pack(pady=10)

        # Nút nhấn đẹp hơn
        self.button = Button(control_frame, text="START / STOP", command=self.on_click, font=("Arial", 14, "bold"),
                             bg="#27ae60", fg="white", activebackground="#2ecc71", activeforeground="white",
                             relief="flat", padx=20, pady=5, bd=3)
        self.button.pack(pady=5)

        # Hiển thị trạng thái (màu thay đổi theo trạng thái)
        self.label = Label(self, text="Stopped", font=("Arial", 12, "bold"), fg="red", bg="#2c3e50")
        self.label.pack()

    def on_click(self):
        self.running = not self.running
        if self.running:
            self.label.config(text="Running", fg="#2ecc71")  # Xanh lá khi chạy
        else:
            self.label.config(text="Stopped", fg="red")  # Đỏ khi dừng

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
