#define LED_PIN 4 // Chân GPIO điều khiển LED

void setup() {
  pinMode(LED_PIN, OUTPUT); // Cấu hình chân LED làm đầu ra
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // Bật LED
  delay(500); // Chờ 500ms
  digitalWrite(LED_PIN, LOW); // Tắt LED
  delay(500); // Chờ 500ms
}
