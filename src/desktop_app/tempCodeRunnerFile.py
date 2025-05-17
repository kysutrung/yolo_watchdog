import tkinter as tk
from tkinter import ttk
import serial

# Thay đổi COM port theo máy bạn, ví dụ: 'COM3' trên Windows hoặc '/dev/ttyUSB0' trên Linux
SERIAL_PORT = 'COM21'
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Không kết nối được với ESP32: {e}")
    ser = None

def send_angle(servo_id, angle):
    if ser and ser.is_open:
        command = f"{servo_id}:{angle}\n"
        ser.write(command.encode())

def on_servo1_change(val):
    send_angle(1, int(float(val)))

def on_servo2_change(val):
    send_angle(2, int(float(val)))

root = tk.Tk()
root.title("Servo Controller")

ttk.Label(root, text="Servo 1").pack()
servo1_slider = ttk.Scale(root, from_=0, to=180, orient='horizontal', command=on_servo1_change)
servo1_slider.set(90)
servo1_slider.pack(padx=10, pady=10)

ttk.Label(root, text="Servo 2").pack()
servo2_slider = ttk.Scale(root, from_=0, to=180, orient='horizontal', command=on_servo2_change)
servo2_slider.set(90)
servo2_slider.pack(padx=10, pady=10)

root.mainloop() 
