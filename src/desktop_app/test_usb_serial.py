import struct
import serial
import time

# Thiết lập cổng serial
ser = serial.Serial('COM10', 115200, timeout=1)

# Danh sách 8 số nguyên
numbers = [0, 0, 0, 0, 0, 0, 0, 0]

numbers[0] = 1
numbers[1] = 1
numbers[2] = 1
numbers[3] = 1
numbers[4] = 66
numbers[5] = 1
numbers[6] = 1
numbers[7] = 1

# Đóng gói dữ liệu thành struct (8 số nguyên 4 byte)
data = struct.pack('8i', *numbers)

# Gửi dữ liệu đến ESP32
ser.write(data)
print("Đã gửi dữ liệu:", numbers)

ser.close()
