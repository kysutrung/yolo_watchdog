import serial
import time

# Cấu hình cổng serial để kết nối với Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Thay đổi '/dev/ttyACM0' nếu cổng khác
time.sleep(2)  # Đợi Arduino khởi động

# Danh sách các số để gửi (chẵn và lẻ)
numbers_to_send = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for number in numbers_to_send:
    # Gửi số đến Arduino
    ser.write(f"{number}\n".encode('utf-8'))
    print(f"Sent: {number}")
    
    # Đợi một chút để Arduino xử lý
    time.sleep(1)

# Đóng kết nối
ser.close()
