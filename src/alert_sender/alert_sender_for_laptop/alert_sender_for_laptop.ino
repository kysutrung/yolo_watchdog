#define LED_PIN 4  // Chân GPIO điều khiển LED

bool lastLEDState = LOW;  // Lưu trạng thái cuối của LED

void setup() {
    pinMode(LED_PIN, OUTPUT);  // Cấu hình chân LED là đầu ra
    Serial.begin(115200);  // Khởi động Serial
    digitalWrite(LED_PIN, lastLEDState);  // Giữ trạng thái cuối khi khởi động
}

void loop() {
    if (Serial.available()) {  // Kiểm tra nếu có dữ liệu Serial
        int receivedNumber = Serial.parseInt();  // Đọc số nguyên từ Serial
        if (receivedNumber % 2 != 0) {  // Nếu là số lẻ
            lastLEDState = HIGH;
        } else {
            lastLEDState = LOW;
        }
        digitalWrite(LED_PIN, lastLEDState);  // Cập nhật LED
    }
}
