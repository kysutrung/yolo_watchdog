import struct
import serial
import time

# Thiết lập cổng serial
ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(2)  # Chờ ESP32 khởi động

# Danh sách 8 số nguyên
numbers = [1, 3, 5, 7, 9, 11, 13, 144]  # Toàn số lẻ để test LED sáng

# Đóng gói dữ liệu thành struct (8 số nguyên 4 byte)
data = struct.pack('8i', *numbers)

# Gửi dữ liệu đến ESP32
ser.write(data)
print("Đã gửi dữ liệu:", numbers)

ser.close()
