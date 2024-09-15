#code nạp bên raspberry pi
#code nạp esp chưa có, tự xây được bằng code sender

import serial
import time
import struct

# Cấu hình cổng serial để kết nối với ESP(kiểm tra cổng trước khi chạy)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Đợi Arduino khởi động

# Danh sách các số để gửi (chẵn và lẻ)
numbers_to_send = [0, 0, 3, 0] #hehe

# Gửi số đến Arduino
# Đóng gói 4 số nguyên thành dữ liệu nhị phân (4 số int 32-bit)
data = struct.pack('4i', *numbers_to_send)
ser.write(data)
print(f"Sent: {numbers_to_send}")

# Đợi một chút để Arduino xử lý
time.sleep(1)

# Đóng kết nối
ser.close()
