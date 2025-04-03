#include "M5StickCPlus2.h"
#include <esp_now.h>
#include <WiFi.h>
#include <string>

typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

int soNhanDuoc[] = {0, 0, 0, 0, 0, 0, 0, 0};
int soNhanDuocCuoi[] = {3, 3, 3, 3, 3, 3, 3, 3};
bool thongBaoDaThayDoi = 0;
bool canhBaoCoi = 0;



void OnDataRecv(const uint8_t *info, const uint8_t *incomingData, int len) {
  memcpy(&packet, incomingData, sizeof(packet));
  Serial.print("Nhận được dữ liệu: ");
  for (int i = 0; i < 8; i++){
    if(packet.numbers[i] != soNhanDuoc[i]){
      soNhanDuoc[i] = packet.numbers[i];
    }
  }
}

bool isAllZero(int arr[8]) {
    for (int i = 0; i < 8; i++) {
        if (arr[i] > 0) {
            return false;  // Nếu có số lớn hơn 0, trả về false ngay lập tức
        }
    }
    return true;  // Nếu không có số nào > 0, trả về true
}

void yoloWatchdog(){
  for(int u = 0; u < 8; u++){
    if(soNhanDuocCuoi[u] != soNhanDuoc[u]){
      thongBaoDaThayDoi = 1;
    }
  }

  if(thongBaoDaThayDoi == 1){
    StickCP2.Display.clear();
    StickCP2.Display.setTextSize(1);
    StickCP2.Display.setCursor(20, 10);
    StickCP2.Display.printf("Alert Status");
    StickCP2.Display.setTextSize(2);
    StickCP2.Display.setCursor(40, 36);
    StickCP2.Display.printf("%d | %d | %d | %d", soNhanDuoc[0], soNhanDuoc[1], soNhanDuoc[2], soNhanDuoc[3]);
    StickCP2.Display.setCursor(40, 70);
    StickCP2.Display.printf("%d | %d | %d | %d", soNhanDuoc[4], soNhanDuoc[5], soNhanDuoc[6], soNhanDuoc[7]);

    StickCP2.Display.setTextSize(1);  
    StickCP2.Display.setCursor(20, 110);
    StickCP2.Display.printf("YOLO WATCHDOG V3.0");

    if(isAllZero(soNhanDuoc)){
      canhBaoCoi = 0;
    }
    else{
      canhBaoCoi = 1;
    }

    for (int i = 0; i < 8; i++) {
      soNhanDuocCuoi[i] = soNhanDuoc[i];
    }
    thongBaoDaThayDoi = 0;      
  }
}

void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);

  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {

  }

  esp_now_register_recv_cb(OnDataRecv);

  StickCP2.Display.setRotation(1);
  StickCP2.Display.setTextColor(WHITE);
  StickCP2.Display.setTextFont(&fonts::FreeSerif9pt7b);
  StickCP2.Speaker.tone(8000, 20);
}

void loop() {
  yoloWatchdog();
  if(canhBaoCoi == 1){
    StickCP2.Speaker.tone(8000, 20);
  }
}
