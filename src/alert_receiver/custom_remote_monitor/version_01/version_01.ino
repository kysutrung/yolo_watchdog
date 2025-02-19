//TFT ST7798
//GPIO 14 ->SCK
//GPIO 13 ->SDA
//GPIO 4  ->RES
//GPIO 21 ->DC
//3.3V    ->BLK
#include <TFT_eSPI.h>  // Thư viện TFT_eSPI
TFT_eSPI tft = TFT_eSPI();  // Khởi tạo đối tượng TFT
#include <esp_now.h>
#include <WiFi.h>

typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

int soNhanDuoc[8];

const int coiPin = 15;


// Hàm callback khi nhận dữ liệu
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
    memcpy(&packet, incomingData, sizeof(packet));
    Serial.print("Nhận được dữ liệu: ");
    for (int i = 0; i < 8; i++) {
      if(packet.numbers[i] != soNhanDuoc[i]){
        soNhanDuoc[i] = packet.numbers[i];
      }
    }
}


//MAIN
void setup() {
  Serial.begin(115200);

  // Đặt ESP32 vào chế độ Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Khởi tạo ESP-NOW
  if (esp_now_init() != ESP_OK) {

  }

  // Đăng ký callback khi nhận dữ liệu
  esp_now_register_recv_cb(OnDataRecv);

  tft.init();  // Khởi tạo màn hình
  tft.setRotation(3);  // Đặt hướng màn hình (0, 90, 180, 270)
  tft.fillScreen(TFT_RED);  // Màu nền đen
  
}

void loop(){
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE);  // Màu chữ
    tft.setTextSize(2);  // Kích thước chữ
    // Hiển thị số nhận được
    tft.setCursor(20, 25);
    tft.print("KV1  KV2  KV3  KV4");
    tft.setCursor(30, 60);
    tft.print(soNhanDuoc[0]);
    tft.setCursor(90, 60);
    tft.print(soNhanDuoc[1]);
    tft.setCursor(150, 60);
    tft.print(soNhanDuoc[2]);
    tft.setCursor(210, 60);
    tft.print(soNhanDuoc[3]);


    tft.setCursor(20, 120);
    tft.print("KV5  KV6  KV7  KV8");
    tft.setCursor(30, 155);
    tft.print(soNhanDuoc[4]);
    tft.setCursor(90, 155);
    tft.print(soNhanDuoc[5]);
    tft.setCursor(150, 155);
    tft.print(soNhanDuoc[6]);
    tft.setCursor(210, 155);
    tft.print(soNhanDuoc[7]); 

    for (int i = 0; i < 8; i++) {
      if(soNhanDuoc[i] > 0){
        tone(coiPin, 700, 100);
      }
    }

    delay(100);
}