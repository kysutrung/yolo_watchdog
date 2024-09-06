import serial
import time
import struct

# Cấu hình cổng serial
ser = serial.Serial('/dev/ttyUSB0', 115200) #check lại khi kết nối cam
time.sleep(2)  # Đợi Arduino khởi động

a = list_a[1]
b = list_a[2]
c = list_a[3]
d = list_a[4]

while True:
    data = struct.pack('iiii', a, b, c, d)
    ser.write(data)
    ser.flush()
    print("OK")
    time.sleep(1)
