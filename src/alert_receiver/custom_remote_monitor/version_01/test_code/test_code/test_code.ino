//==========SƠ ĐỒ ĐẤU NỐI=========
//TFT ST7798
//GPIO 14 ->SCK
//GPIO 13 ->SDA
//GPIO 4  ->RES
//GPIO 21 ->DC
//3.3V    ->BLK
//CÒI -> GPIO 15
//NÚT BẤM
//=================================

#include <TFT_eSPI.h>  // Thư viện TFT_eSPI
TFT_eSPI tft = TFT_eSPI();  // Khởi tạo đối tượng TFT
#include <esp_now.h>
#include <WiFi.h>

typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

//GLOBAL VAR
unsigned long lastReceiveTime = 0;
const unsigned long timeout = 3000; // 5 giây

const int coiPin = 15;
const int nutMot = 25;
const int nutHai = 33;
const int nutBa = 32;

bool trangThaiNut1Truoc = HIGH;
bool trangThaiNut2Truoc = HIGH;
bool trangThaiNut3Truoc = HIGH;

bool thayDoi = 0;

int soNhanDuoc[] = {0, 0, 0, 0, 0, 0, 0, 0};
int soNhanDuocCuoi[] = {3, 3, 3, 3, 3, 3, 3, 3};

int MENU_MODE = 9;
int TRANG_THAI_COI = 2;
int TRANG_THAI_COI_CUOI = 3;
int BIEN_NHO_HUONG_DAN = 0;


// Hàm callback khi nhận dữ liệu
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  memcpy(&packet, incomingData, sizeof(packet));
  Serial.print("Nhận được dữ liệu: ");
  for (int i = 0; i < 8; i++){
    if(packet.numbers[i] != soNhanDuoc[i]){
      soNhanDuoc[i] = packet.numbers[i];
    }
  }

  lastReceiveTime = millis();
}

void datMauChu(int numA){
  if(numA == 0){
    tft.setTextColor(TFT_GREEN);
  }
  else{
    tft.setTextColor(TFT_RED);
  }
}

void coiCanhBao(){
  for (int i = 0; i < 8; i++) {
    if(soNhanDuoc[i] > 0 && TRANG_THAI_COI == 1){
      tone(coiPin, 500, 100);
    }
  }
}

void xemCanhBao(){
  for(int u = 0; u < 8; u++){
    if(soNhanDuocCuoi[u] != soNhanDuoc[u]){
      thayDoi = 1;
    }
  }

  if(TRANG_THAI_COI_CUOI != TRANG_THAI_COI){
    thayDoi = 1;
  }

  if(millis() - lastReceiveTime > timeout){
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_RED);  // Màu chữ
    // Hiển thị số nhận được
    tft.setCursor(40, 100);
    tft.print("Lost Connection !");
  }

  if(thayDoi){
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE);  // Màu chữ
    // Hiển thị số nhận được
    tft.setCursor(20, 25);
    tft.print("Z1        Z2        Z3        Z4");

    datMauChu(soNhanDuoc[0]);
    tft.setCursor(20, 60);
    tft.print(soNhanDuoc[0]);
    datMauChu(soNhanDuoc[1]);
    tft.setCursor(80, 60);
    tft.print(soNhanDuoc[1]);
    datMauChu(soNhanDuoc[2]);
    tft.setCursor(140, 60);
    tft.print(soNhanDuoc[2]);
    datMauChu(soNhanDuoc[3]);
    tft.setCursor(200, 60);
    tft.print(soNhanDuoc[3]);

    tft.setTextColor(TFT_WHITE);
    tft.setCursor(20, 120);
    tft.print("Z5        Z6        Z7        Z8");
    datMauChu(soNhanDuoc[4]);
    tft.setCursor(20, 155);
    tft.print(soNhanDuoc[4]);
    datMauChu(soNhanDuoc[5]);
    tft.setCursor(80, 155);
    tft.print(soNhanDuoc[5]);
    datMauChu(soNhanDuoc[6]);
    tft.setCursor(140, 155);
    tft.print(soNhanDuoc[6]);
    datMauChu(soNhanDuoc[7]);
    tft.setCursor(200, 155);
    tft.print(soNhanDuoc[7]);

    tft.setCursor(20, 210);
    if(TRANG_THAI_COI == 1){
      tft.setTextColor(TFT_WHITE);
      tft.print("Alarm: On");
    }
    else if(TRANG_THAI_COI == 2){
      tft.setTextColor(TFT_BLUE);
      tft.print("Alarm: Off");
    }

    coiCanhBao();
    
    for (int i = 0; i < 8; i++) {
      soNhanDuocCuoi[i] = soNhanDuoc[i];
    }

    TRANG_THAI_COI_CUOI = TRANG_THAI_COI;
    thayDoi = 0;
  }

  BIEN_NHO_HUONG_DAN = 0;
}

void thongTin(){
  if(BIEN_NHO_HUONG_DAN == 0){
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_RED);  // Màu chữ
    // Hiển thị số nhận được
    tft.setCursor(20, 25);
    tft.print("YOLO WATCHDOG V3.0");
    tft.setCursor(20, 50);
    tft.print("Remote Monitor Unit");
    tft.setTextColor(TFT_WHITE);  // Màu chữ
    tft.setCursor(20, 80);
    tft.print("The function of this device");
    tft.setCursor(20, 105);
    tft.print("is to notify of the number of");
    tft.setCursor(20, 130);
    tft.print("violations in each specific");
    tft.setCursor(20, 155);
    tft.print("monitored area.");  
    tft.setCursor(20, 190);
    tft.setTextColor(TFT_RED);  // Màu chữ
    tft.print("Designed by Trungtaulua");
    tft.setCursor(20, 215);
    tft.print("April 2025");
    tft.setTextColor(TFT_WHITE);  // Màu chữ
    BIEN_NHO_HUONG_DAN = 3;
    thayDoi = 1;
  }
}

void hienThiManHinh(){
  if(MENU_MODE == 2){
    xemCanhBao();
  }
  else if(MENU_MODE == 1){
    thongTin();
  }
  else{

  }
}


void nhanNut() {
  int trangThaiNut1 = digitalRead(nutMot);
  int trangThaiNut2 = digitalRead(nutHai);
  int trangThaiNut3 = digitalRead(nutBa);

  if (trangThaiNut1 == LOW && trangThaiNut1Truoc == HIGH) {
    if (digitalRead(nutMot) == LOW) {
      MENU_MODE = 1;
    }
  }

  if (trangThaiNut2 == LOW && trangThaiNut2Truoc == HIGH) {
    if (digitalRead(nutHai) == LOW) {
      MENU_MODE = 2;
    }
  }

  if (trangThaiNut3 == LOW && trangThaiNut3Truoc == HIGH) {
    if (digitalRead(nutBa) == LOW) {
      TRANG_THAI_COI++;
      if(TRANG_THAI_COI > 2){
        TRANG_THAI_COI = 1;
      }
    }
  }

  trangThaiNut1Truoc = trangThaiNut1;
  trangThaiNut2Truoc = trangThaiNut2;
  trangThaiNut3Truoc = trangThaiNut3;
}

void chiDanNut(){
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE);  // Màu chữ
    // Hiển thị số nhận được
    tft.setCursor(20, 25);
    tft.print("Thong Tin ------>");
    tft.setCursor(20, 110);
    tft.print("Thong Bao ------>");
    tft.setCursor(20, 200);
    tft.print("Bat/Tat Coi ------>");
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
  tft.setFreeFont(&FreeSerif9pt7b);
  tft.setTextSize(1);  // Kích thước chữ
  tft.setRotation(0);  // Đặt hướng màn hình (0, 90, 180, 270)
  tft.fillScreen(TFT_RED);  // Màu nền đen

  chiDanNut();
  
  pinMode(coiPin, OUTPUT);
  pinMode(nutMot, INPUT_PULLUP);
  pinMode(nutHai, INPUT_PULLUP);
  pinMode(nutBa, INPUT_PULLUP);
}

void loop(){
  nhanNut();
  hienThiManHinh();
}