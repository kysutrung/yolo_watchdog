import cv2

cap = cv2.VideoCapture(0)

_, first_frame = cap.read()
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    delta_frame = cv2.absdiff(first_gray, gray)
    _, thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)
    cv2.imshow("Motion", thresh)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
