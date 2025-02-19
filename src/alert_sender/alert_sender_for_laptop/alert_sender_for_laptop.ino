#include <Arduino.h>

#define LED_PIN 4  // Chân GPIO4 để điều khiển LED

void setup() {
    Serial.begin(115200);  // Kết nối với laptop
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);  // Ban đầu tắt LED
}

void loop() {
    if (Serial.available() >= 32) {  // Mỗi int32 = 4 byte, 8 số = 32 byte
        int numbers[8];
        Serial.readBytes((char*)numbers, 32);  // Nhận dữ liệu vào mảng

        bool allEven = true;
        for (int i = 0; i < 8; i++) {
            if (numbers[i] % 2 != 0) {
                allEven = false;
                break;
            }
        }

        // Bật LED nếu tất cả số là số lẻ
        if (allEven) {
            digitalWrite(LED_PIN, LOW);
        } else {
            digitalWrite(LED_PIN, HIGH);
        }
    }
}
