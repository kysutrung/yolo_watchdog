#define LED_PIN 4 // Chân GPIO điều khiển LED

void setup() {
  pinMode(LED_PIN, OUTPUT); // Cấu hình chân LED làm đầu ra
  Serial.begin(115200); // Khởi động Serial
}

void loop() {
  if (Serial.available()) { // Kiểm tra nếu có dữ liệu Serial
    int receivedNumber = Serial.parseInt(); // Đọc số nguyên từ Serial
    if (receivedNumber % 2 != 0) { // Nếu là số lẻ
      digitalWrite(LED_PIN, HIGH); // Bật LED
    } else {
      digitalWrite(LED_PIN, LOW); // Tắt LED
    }
  }
}
