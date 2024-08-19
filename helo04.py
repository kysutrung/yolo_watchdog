import cv2

# Mở kết nối với camera
cap = cv2.VideoCapture(0)

# Đọc và xử lý khung hình đầu tiên
_, first_frame = cap.read()
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

while True:
    # Đọc khung hình hiện tại
    _, frame = cap.read()
    
    # Chuyển đổi khung hình sang thang độ xám và làm mờ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Tính toán sự khác biệt và ngưỡng
    delta_frame = cv2.absdiff(first_gray, gray)
    _, thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)
    
    # Lấy kích thước khung hình
    height, width = frame.shape[:2]
    
    # Tính toán tọa độ để chia khung hình thành 9 ô
    third_x = width // 3
    third_y = height // 3
    
    # Vẽ các đường kẻ dọc để chia khung hình thành 3 cột
    cv2.line(thresh, (third_x, 0), (third_x, height), (255, 255, 255), 2)
    cv2.line(thresh, (2 * third_x, 0), (2 * third_x, height), (255, 255, 255), 2)
    
    # Vẽ các đường kẻ ngang để chia khung hình thành 3 hàng
    cv2.line(thresh, (0, third_y), (width, third_y), (255, 255, 255), 2)
    cv2.line(thresh, (0, 2 * third_y), (width, 2 * third_y), (255, 255, 255), 2)
    
    # Hiển thị số thứ tự trên các ô
    for i in range(3):
        for j in range(3):
            # Tính toán tọa độ của ô hiện tại
            x = j * third_x
            y = i * third_y
            # Tọa độ của vị trí để hiện số
            text_position = (x + third_x // 2 - 10, y + third_y // 2 + 10)
            # Hiện số thứ tự (từ 1 đến 9)
            cv2.putText(thresh, str(i * 3 + j + 1), text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Hiển thị khung hình phát hiện chuyển động với các đường kẻ và số thứ tự
    cv2.imshow("Motion Detection", thresh)
    
    # Điều kiện để thoát vòng lặp khi nhấn phím 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
