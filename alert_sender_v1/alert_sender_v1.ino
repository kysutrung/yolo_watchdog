//code cho esp32 nhận tín hiệu từ RP3 qua usb serial
//gửi tín hiệu qua một esp32 khác bằng NOW

/*
NỘI DUNG ĐIỂU KHIỂN
 - nhận tín hiệu từ RP3 dưới dạng struct
  led now - báo now khởi tạo có thành công không
  led nguồn - báo có điện
  led vị trí - báo dựa trên cái struct nhận được
*/

//khai báo chân
#define LED_NOW 13
#define LED_KV1 12
#define LED_KV2 14
#define LED_KV3 27
#define LED_KV4 26

//thư viện cho now
#include <esp_now.h>
#include <WiFi.h>

//địa chỉ MAC của ESP32 Nhận
uint8_t receiverMAC[] = {0xB0, 0xA7, 0x32, 0x2F, 0xA7, 0xC8};

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

  // Thiết lập chân
  pinMode(LED_NOW, OUTPUT);
  pinMode(LED_KV1, OUTPUT);
  pinMode(LED_KV2, OUTPUT);
  pinMode(LED_KV3, OUTPUT);
  pinMode(LED_KV4, OUTPUT);

  // Tắt hết đèn ban đầu
  digitalWrite(LED_NOW, LOW);
  digitalWrite(LED_KV1, LOW);
  digitalWrite(LED_KV2, LOW);
  digitalWrite(LED_KV3, LOW);
  digitalWrite(LED_KV4, LOW);
  
  // Khởi động Wi-Fi ở chế độ Station (trạm)
  WiFi.mode(WIFI_STA);
  
  // Khởi động ESP-NOW
  if (esp_now_init() != ESP_OK) {
    digitalWrite(LED_NOW, HIGH);
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


void loop() {
  
  //kiểm tra xem có dữ liệu đến từ Raspberry Pi không
  if (Serial.available() >= 16) {
  //đọc dữ liệu và chuyển đổi thành số nguyên
  int so_tu_usb[4];
  Serial.readBytes((char*)so_tu_usb, 16);
  
  myData.number_1 = so_tu_usb[0];
  myData.number_2 = so_tu_usb[1];
  myData.number_3 = so_tu_usb[2];
  myData.number_4 = so_tu_usb[3];

  esp_err_t result = esp_now_send(receiverMAC, (uint8_t *) &myData, sizeof(myData));
  
  //điều khiển đèn
  if(so_tu_usb[0] > 0){
    digitalWrite(LED_KV1, HIGH);
  }
  else{
    digitalWrite(LED_KV1, LOW);
  }

  if(so_tu_usb[1] > 0){
    digitalWrite(LED_KV2, HIGH);
  }
  else{
    digitalWrite(LED_KV2, LOW);
  }

  if(so_tu_usb[2] > 0){
    digitalWrite(LED_KV3, HIGH);
  }
  else{
    digitalWrite(LED_KV3, LOW);
  }
  
  if(so_tu_usb[3] > 0){
    digitalWrite(LED_KV4, HIGH);
  }
  else{
    digitalWrite(LED_KV4, LOW);
  }

  } 
}
