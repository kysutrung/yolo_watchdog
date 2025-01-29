//code test gửi số qua now

//thư viện cho now
#include <esp_now.h>
#include <WiFi.h>

//địa chỉ MAC của ESP32 Nhận
uint8_t receiverMAC[] = {0x10, 0x06, 0x1C, 0x27, 0xEF, 0x14};

//cấu trúc dữ liệu để gửi
typedef struct struct_message {
  int number_1;
  int number_2;
  int number_3;
  int number_4;
} struct_message;

struct_message myData;

void setup() {
  // Khởi động Serial Monitor
  Serial.begin(9600);

  // Khởi động Wi-Fi ở chế độ Station (trạm)
  WiFi.mode(WIFI_STA);
  
  // Khởi động ESP-NOW
  if (esp_now_init() != ESP_OK) {
    
  }
  
  // Đăng ký địa chỉ MAC của ESP32 Nhận (Receiver)
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }

}


void loop(){
  
  myData.number_1 = 1;
  myData.number_2 = 2;
  myData.number_3 = 3;
  myData.number_4 = 0;

  esp_err_t result = esp_now_send(receiverMAC, (uint8_t *) &myData, sizeof(myData));
  Serial.println(result);
  
}
