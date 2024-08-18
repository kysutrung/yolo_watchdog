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
    
    # Tính toán tọa độ của tâm khung hình
    center_x, center_y = width // 2, height // 2
    
    # Vẽ đường kẻ dọc qua tâm trên khung hình phát hiện chuyển động
    cv2.line(thresh, (center_x, 0), (center_x, height), (255, 255, 255), 5)
    
    # Vẽ đường kẻ ngang qua tâm trên khung hình phát hiện chuyển động
    cv2.line(thresh, (0, center_y), (width, center_y), (255, 255, 255), 5)
    
    # Hiển thị khung hình phát hiện chuyển động với các đường kẻ
    cv2.imshow("Motion Detection", thresh)
    
    # Điều kiện để thoát vòng lặp khi nhấn phím 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
