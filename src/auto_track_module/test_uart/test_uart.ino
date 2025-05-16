#include <Arduino.h>

void setup() {
  // Khởi động cổng nối tiếp để giao tiếp với máy tính (USB)
  Serial.begin(115200);  // Tốc độ baudrate là 115200
  while (!Serial) {
    ; // Đợi ESP32 kết nối cổng USB
  }
  Serial.println("ESP32 is ready to receive coordinates.");
}

void loop() {
  // Kiểm tra xem có dữ liệu nào đến không
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Đọc dữ liệu đến dấu xuống dòng

    // Tách tọa độ x và y từ chuỗi dữ liệu
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      String x_str = data.substring(0, commaIndex);
      String y_str = data.substring(commaIndex + 1);

      int center_x = x_str.toInt();
      int center_y = y_str.toInt();

      // In tọa độ tâm ra terminal
      Serial.print("Received center coordinates: ");
      Serial.print("X: ");
      Serial.print(center_x);
      Serial.print(" Y: ");
      Serial.println(center_y);
    }
  }
}
