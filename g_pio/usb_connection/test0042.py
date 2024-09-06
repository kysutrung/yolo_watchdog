import serial
import time
import struct

# Cấu hình cổng serial để kết nối với Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

num_a = 0

for number in range(0, 10):
    a = num_a
    b = num_a
    c = num_a
    d = num_a
    data = struct.pack('iiii', a, b, c, d)
    ser.write(data.encode('utf-8'))
    print(f"Sent: {number}")
    num_a += 1
    # Đợi một chút để Arduino xử lý
    time.sleep(1)

# Đóng kết nối
ser.close()
