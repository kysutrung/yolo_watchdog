//nhận tín hiệu từ RP3 qua usb serial
//gửi tín hiệu qua một esp32 khác bằng NOW

#include <esp_now.h>
#include <WiFi.h>
uint8_t diaChiMACNhan[] = {1, 2, 3, 4, 5, 6};

#define ledNow 14

struct duLieu {
  int khuVuc;
  int soLuong;
};

void setup() {
  // Khởi động serial để nhận dữ liệu từ Raspberry Pi
  Serial.begin(115200);

  // Khởi động Wi-Fi ở chế độ Station (trạm)
  WiFi.mode(WIFI_STA);
  // Bật đèn báo Now có hoạt động
  pinMode(ledNow, OUTPUT);
  digitalWrite(ledNow, HIGH);

  // Khởi động ESP-NOW
  if (esp_now_init() != ESP_OK) {
    digitalWrite(ledNow, LOW);
  }

  // Đăng ký địa chỉ MAC của ESP32 Nhận
  esp_now_peer_info_t infoBenNhan;
  memcpy(infoBenNhan.peer_addr, diaChiMACNhan, 6);
  infoBenNhan.channel = 0;
  infoBenNhan.encrypt = false;

  if (esp_now_add_peer(&infoBenNhan) != ESP_OK) {
    digitalWrite(ledNow, LOW);
  }
}

void loop() {
    //khởi tạo một biến chứa dữ liệu
    duLieu duLieuTuRP3;
    // Kiểm tra nếu có đủ dữ liệu cho struct
    if (Serial.available() >= sizeof(duLieuTuRP3)) {
        // Đọc dãy byte và lưu vào struct
        Serial.readBytes((uint8_t*)&duLieuTuRP3, sizeof(duLieuTuRP3));
        // Gửi struct qua ESP-NOW
        esp_err_t phanHoi = esp_now_send(diaChiMACNhan, (uint8_t *) &duLieuTuRP3, sizeof(duLieuTuRP3));
        if (phanHoi != ESP_OK) {
            digitalWrite(ledNow, LOW);
        } 
    }
}