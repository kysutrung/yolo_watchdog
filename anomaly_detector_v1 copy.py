import serial
import time
import struct

# Cấu hình cổng serial
ser = serial.Serial('/dev/ttyUSB0', 115200) #check lại khi kết nối cam
time.sleep(2)  # Đợi Arduino khởi động

num_a = 0

while True:
    a = list_a[num_a]
    b = list_a[num_a]
    c = list_a[num_a]
    d = list_a[num_a]
    data = struct.pack('iiii', a, b, c, d)
    ser.write(data)
    ser.flush()
    print("OK")
    time.sleep(1)
    num += 1
