import serial
import time

# Cấu hình cổng Serial (thay đổi COMx cho Windows hoặc /dev/ttyUSBx cho Linux/macOS)
SERIAL_PORT = "COM10"  # Thay đổi nếu cần
BAUD_RATE = 115200  # Phải khớp với ESP32

# Giá trị số muốn gửi (chỉnh sửa tại đây)
number_to_send = 31  # Thay đổi số này theo ý muốn

try:
    # Mở cổng Serial
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Đợi ESP32 khởi động

    # Gửi số một lần
    ser.write(f"{number_to_send}\n".encode())  
    print(f"Đã gửi: {number_to_send}")

except serial.SerialException:
    print("Không thể mở cổng Serial. Kiểm tra kết nối ESP32!")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()  # Đóng cổng Serial khi hoàn thành
        print("Đã đóng kết nối Serial.")
