import serial
import time
import struct

# Cấu hình cổng serial để kết nối với Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Đợi Arduino khởi động

# Danh sách các số để gửi (chẵn và lẻ)
numbers_to_send = [1, 2, 3, 4] #hehe

for number in numbers_to_send:
    # Gửi số đến Arduino
    # Đóng gói 4 số nguyên thành dữ liệu nhị phân (4 số int 32-bit)
    data = struct.pack('4i', *numbers_to_send)
    ser.write(data.encode('utf-8'))
    print(f"Sent: {numbers_to_send}")
    
    # Đợi một chút để Arduino xử lý
    time.sleep(1)

# Đóng kết nối
ser.close()
