import tkinter as tk
from tkinter import ttk

class FruitStorageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Thùng Trái Cây")
        self.geometry("400x250")

        # Danh sách thùng & loại quả
        self.bins = ["Thùng 1", "Thùng 2", "Thùng 3"]
        self.fruits = ["Banana", "Apple", "Orange"]

        # Lưu danh sách trái cây đã chọn cho từng thùng
        self.bin_fruit_selection = {bin_name: {fruit: tk.BooleanVar() for fruit in self.fruits} for bin_name in self.bins}

        # Tạo khung chứa nội dung
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # **Cột bên trái: Chọn thùng**
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", padx=10, fill="y")

        self.bin_label = tk.Label(self.left_frame, text="Chọn Thùng", font=("Arial", 12, "bold"))
        self.bin_label.pack(pady=5)

        self.selected_bin = tk.StringVar()
        self.bin_combobox = ttk.Combobox(self.left_frame, values=self.bins, textvariable=self.selected_bin, state="readonly")
        self.bin_combobox.pack()
        self.bin_combobox.bind("<<ComboboxSelected>>", self.update_checkboxes)

        # **Cột bên phải: Chọn loại quả**
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", padx=10, fill="both", expand=True)

        self.fruit_label = tk.Label(self.right_frame, text="Chọn Loại Trái Cây", font=("Arial", 12, "bold"))
        self.fruit_label.pack(pady=5)

        self.checkbox_frame = tk.Frame(self.right_frame)
        self.checkbox_frame.pack()

        # Tạo các checkbox (ẩn ban đầu)
        self.checkboxes = {fruit: tk.Checkbutton(self.checkbox_frame, text=fruit) for fruit in self.fruits}
        for fruit, checkbox in self.checkboxes.items():
            checkbox.pack(anchor="w")

        # Nút xác nhận
        self.button = tk.Button(self, text="Xác nhận", command=self.show_selected)
        self.button.pack(pady=10)

        # Label hiển thị kết quả
        self.result_label = tk.Label(self, text="Chưa chọn thùng", font=("Arial", 12))
        self.result_label.pack()

    def update_checkboxes(self, event):
        """Cập nhật checkbox khi chọn thùng"""
        bin_name = self.selected_bin.get()
        if not bin_name:
            return

        # Cập nhật trạng thái checkbox theo dữ liệu của thùng đã chọn
        for fruit, checkbox in self.checkboxes.items():
            checkbox.config(variable=self.bin_fruit_selection[bin_name][fruit])

    def show_selected(self):
        """Hiển thị loại trái cây đã chọn cho từng thùng"""
        result_text = ""
        for bin_name, fruit_selection in self.bin_fruit_selection.items():
            selected_fruits = [fruit for fruit, var in fruit_selection.items() if var.get()]
            result_text += f"{bin_name}: {', '.join(selected_fruits) if selected_fruits else 'Không có'}\n"

        self.result_label.config(text=result_text)

if __name__ == "__main__":
    app = FruitStorageApp()
    app.mainloop()
