#include <M5StickCPlus2.h>  // Thư viện M5StickC

void setup() {
  // Khởi động M5StickC
    auto cfg = M5.config();
    StickCP2.begin(cfg);
  
  // Khởi động Serial để in ra kết quả
  Serial.begin(115200);

  // Lấy địa chỉ MAC Wi-Fi của ESP32
  uint8_t mac[6];
  esp_read_mac(mac, ESP_MAC_WIFI_STA); // Lấy địa chỉ MAC của Wi-Fi Station

  // In ra địa chỉ MAC theo định dạng tiêu chuẩn
  Serial.print("Địa chỉ MAC của thiết bị là: ");
  for (int i = 0; i < 6; i++) {
    if (i != 0) Serial.print(":");
    Serial.print(mac[i], HEX); // In ra từng byte của MAC dưới dạng hex
  }
  Serial.println();
}

void loop() {
  M5.update();

  // Kiểm tra xem nút A có được nhấn hay không
  if (M5.BtnA.wasPressed()) {
    Serial.println("Đang khởi động lại...");
    esp_restart();  // Hàm này sẽ reset thiết bị
  }
}