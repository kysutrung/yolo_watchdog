import serial
import time
import struct

# Cấu hình cổng serial
ser = serial.Serial('/dev/ttyACM0', 115200) #check lại khi kết nối cam
time.sleep(2)  # Đợi Arduino khởi động

num_a = 0

while True:
    a = num_a
    b = num_a
    c = num_a
    d = num_a
    data = struct.pack('iiii', a, b, c, d)
    ser.write(data)
    ser.flush()       
    print("OK")
    time.sleep(1)
    num_a += 1
    time.sleep(2) 
