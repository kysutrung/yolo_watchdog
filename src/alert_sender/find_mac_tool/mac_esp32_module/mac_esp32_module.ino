#include <WiFi.h>
#include "esp_wifi.h" 

void setup() {
  Serial.begin(115200);
  Serial.println();
  WiFi.begin();
  // Khởi động WiFi ở chế độ Station để lấy địa chỉ MAC
  WiFi.mode(WIFI_STA);
  Serial.print("Wi-Fi MAC Address: ");
  Serial.println(WiFi.macAddress());
}

void loop() {
  // Không cần làm gì trong loop
}