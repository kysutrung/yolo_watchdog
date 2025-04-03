//CHƯƠNG TRÌNH TẠO GIAO DIỆN NGƯỜI DÙNG ĐƠN GIẢN CHO ESP32 dựa trên một số hàm có sẵn của M5Stack
//CÓ THỂ DÙNG CHO NHIỀU DỰ ÁN
//DỰ ÁN ĐANG TEST: YOLO WATCHDOG

#include "M5StickCPlus2.h"  // Đọc tài liệu để cài thư viện M5StickC Plus 2
#include <esp_now.h>
#include <WiFi.h>

//Global Var
//thời gian kêu còi
uint32_t duration_a = 100;
//lưu thông tin cảnh báo
int g = 0;
int h = 0;
int i = 0;
int k = 0;
//khống chế vòng lặp chế độ
bool x = 0;
//khống chế cơ chế bấm nút
int num_a = -1;
int num_b = -1;
int num_c = 0;
//lưu thông tin cài đặt của từng khu vực
char khuVuc1Cam = 'k';
char khuVuc2Cam = 'k';
char khuVuc3Cam = 'k';
char khuVuc4Cam = 'k';
//dùng để hiển thị màn hình intro
bool daChayIntro = 0;

// 'lulu', 240x135px


//cấu trúc của gói dữ liệu nhận
typedef struct struct_message {
  int number_1;
  int number_2;
  int number_3;
  int number_4;
} struct_message;

// Khởi tạo cấu trúc dữ liệu
struct_message incomingData;

// Hàm callback khi nhận được dữ liệu
void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
  
  if(incomingData.number_1 > 0 || incomingData.number_2 >0 || incomingData.number_3 >0 || incomingData.number_4 >0){
    if(khuVuc1Cam == 'a' || khuVuc2Cam == 'a' || khuVuc3Cam == 'a' || khuVuc4Cam == 'a'){
      StickCP2.Speaker.tone(4000, duration_a);
    }
    g = incomingData.number_1;
    h = incomingData.number_2;
    i = incomingData.number_3;
    k = incomingData.number_4;
  }
}

void chonDoiTuongCam(char n){
  if(n == 'a'){
    StickCP2.Display.fillRect(5, 43, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Cam nguoi");

    StickCP2.Display.setTextColor(WHITE);

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Cho phep tat ca");

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Phai co nguoi");
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.print(" NA");
  }
  if(n == 'b'){
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Cam nguoi");

    StickCP2.Display.fillRect(5, 73, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Cho phep tat ca");

    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Phai co nguoi");
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.print(" NA");
  }
  if(n == 'c'){
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Cam nguoi");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Cho phep tat ca");

    StickCP2.Display.fillRect(5, 103, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Phai co nguoi");
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.print(" NA");
  }
}

void caiDatKV1(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("_Cai dat KV1_____");

    if(num_c == 1){
      khuVuc1Cam = 'a';
    }
    if(num_c == 2){
      khuVuc1Cam = 'b';
    }
    if(num_c == 3){
      khuVuc1Cam = 'c';
    }
    if(num_c == 4){
      num_c = 1;
      khuVuc1Cam = 'a';
    }   

    chonDoiTuongCam(khuVuc1Cam);
    
    x = 1;
  }
}

void caiDatKV2(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("_Cai dat KV2_____");

    if(num_c == 1){
      khuVuc2Cam = 'a';
    }
    if(num_c == 2){
      khuVuc2Cam = 'b';
    }
    if(num_c == 3){
      khuVuc2Cam = 'c';
    }
    if(num_c == 4){
      num_c = 1;
      khuVuc2Cam = 'a';
    }   

    chonDoiTuongCam(khuVuc2Cam);
    
    x = 1;
  }
}

void caiDatKV3(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("_Cai dat KV3_____");

    if(num_c == 1){
      khuVuc3Cam = 'a';
    }
    if(num_c == 2){
      khuVuc3Cam = 'b';
    }
    if(num_c == 3){
      khuVuc3Cam = 'c';
    }
    if(num_c == 4){
      num_c = 1;
      khuVuc3Cam = 'a';
    }   

    chonDoiTuongCam(khuVuc3Cam);
    
    x = 1;
  }
}

void caiDatKV4(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("_Cai dat KV4_____");

    if(num_c == 1){
      khuVuc4Cam = 'a';
    }
    if(num_c == 2){
      khuVuc4Cam = 'b';
    }
    if(num_c == 3){
      khuVuc4Cam = 'c';
    }
    if(num_c == 4){
      num_c = 1;
      khuVuc4Cam = 'a';
    }   

    chonDoiTuongCam(khuVuc4Cam);
    
    x = 1;
  }
}

void onlineMode(){
  if(num_c > 0){
      StickCP2.Display.clear();
      StickCP2.Display.setCursor(20, 20);
      StickCP2.Display.setTextColor(WHITE);
      StickCP2.Display.print("ONLINE");
      StickCP2.Display.setTextColor(GREEN);

      if(incomingData.number_1 > 0 && khuVuc1Cam == 'a'){
        StickCP2.Display.setTextColor(RED);
        StickCP2.Display.setCursor(20, 45);
        StickCP2.Display.print("KV1: ");
        StickCP2.Display.print(g);
        StickCP2.Display.print(" nguoi");
      }
      else{
        StickCP2.Display.setTextColor(GREEN);
        StickCP2.Display.setCursor(20, 45);
        StickCP2.Display.print("KV1: An toan");
      }

      if(incomingData.number_2 > 0 && khuVuc2Cam == 'a'){
        StickCP2.Display.setTextColor(RED);
        StickCP2.Display.setCursor(20, 65);
        StickCP2.Display.print("KV2: ");
        StickCP2.Display.print(h);
        StickCP2.Display.print(" nguoi");
      }
      else{
        StickCP2.Display.setTextColor(GREEN);
        StickCP2.Display.setCursor(20, 65);
        StickCP2.Display.print("KV2: An toan");
      }

      if(incomingData.number_3 > 0 && khuVuc3Cam == 'a'){
        StickCP2.Display.setTextColor(RED);
        StickCP2.Display.setCursor(20, 85);
        StickCP2.Display.print("KV3: ");
        StickCP2.Display.print(i);
        StickCP2.Display.print(" nguoi");
      }
      else{
        StickCP2.Display.setTextColor(GREEN);
        StickCP2.Display.setCursor(20, 85);
        StickCP2.Display.print("KV3: An toan");
      }

      if(incomingData.number_4 > 0 && khuVuc4Cam == 'a'){
        StickCP2.Display.setTextColor(RED);
        StickCP2.Display.setCursor(20, 105);
        StickCP2.Display.print("KV4: ");
        StickCP2.Display.print(k);
        StickCP2.Display.print(" nguoi");
      }
      else{
        StickCP2.Display.setTextColor(GREEN);
        StickCP2.Display.setCursor(20, 105);
        StickCP2.Display.print("KV4: An toan");
      }

      StickCP2.Display.drawRect(5, 0, 235, 135, GREEN); //vẽ hình dạng viền

      delay(100);
  }
}

void hienThiMode(int var_a){

  StickCP2.Display.clear();
  StickCP2.Display.setTextColor(WHITE);
  StickCP2.Display.setCursor(20, 15);
  StickCP2.Display.print("_Cai dat_________");

  if(var_a == 1){
    //StickCP2.Display.fillCircle(25, 22, 5, GREEN);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 43, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.setTextColor(WHITE);

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 3");    
  }

  if(var_a == 2){
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.fillRect(5, 73, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setTextColor(WHITE);

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 3");  
  }

  if(var_a == 3){
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.fillRect(5, 103, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 3");     
  }

  if(var_a == 4){
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.fillRect(5, 103, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 4");  
    
  }

  if(var_a == 5){
    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 4");

    StickCP2.Display.fillRect(5, 103, 235, 20 , WHITE); //vẽ hình dạng fill hình có màu
    StickCP2.Display.setTextColor(BLACK);
    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Xac nhan");  
    
  }

}

void luaChonMode(){
  StickCP2.update();
  if(StickCP2.BtnA.wasClicked()){
    num_a++;
    num_c = 0;
    x = 0;
  }

  if(num_a == 5){
    num_a = 0;
  }

  if(StickCP2.BtnB.wasClicked()){
    num_c++;
    x = 0;
  }

  if(num_a != num_b){
    if(num_a == 0){
      hienThiMode(1);
    }

    if(num_a == 1){
      hienThiMode(2);
    }

    if(num_a == 2){
      hienThiMode(3);
    }

    if(num_a == 3){
      hienThiMode(4);
    }

    if(num_a == 4){
      hienThiMode(5);
    }

    num_b = num_a;
  }

  if(num_a == 0){
    if(num_c > 0){
      caiDatKV1();
    }
  }

  if(num_a == 1){
    if(num_c > 0){
      caiDatKV2();
    }
  }

  if(num_a == 2){
    if(num_c > 0){
      caiDatKV3();
    }
  }

  if(num_a == 3){
    if(num_c > 0){
      caiDatKV4();
    }
  }

  if(num_a == 4){
    if(num_c > 0){
      onlineMode();
    }
  }
}

void hienThiIntro(){
  // Cú pháp: drawBitmap(x, y, width, height, data, color)
  StickCP2.Display.drawBitmap(0, 0, 240, 135, lulu, TFT_BLACK);
  StickCP2.Display.setTextColor(BLACK);
  StickCP2.Display.setCursor(15, 110);
  StickCP2.Display.print("Loading");
  delay(1000);
  StickCP2.Display.print(".");
  delay(1000);
  StickCP2.Display.print(".");
  delay(1000);
  StickCP2.Display.print(".");
  delay(1000);
  StickCP2.Display.print(".");
  delay(1000);
  StickCP2.Display.clear();
  StickCP2.Display.setTextColor(WHITE);
  StickCP2.Display.setCursor(15, 30);
  StickCP2.Display.print("ISI Lab - ISVNU");
  StickCP2.Display.setCursor(15, 60);
  StickCP2.Display.print("YOLO WATCHDOG v1.0");
  StickCP2.Display.setCursor(15, 90);
  StickCP2.Display.setTextSize(1);
  StickCP2.Display.print("Nhan M5 de tiep tuc");
  StickCP2.Display.setTextSize(2);
}

void setup() {
    // Cấu hình và khởi động M5StickC Plus 2
    auto cfg = M5.config();
    StickCP2.begin(cfg);

    // Khởi động Wi-Fi ở chế độ Station (trạm)
    WiFi.mode(WIFI_STA);
    // Khởi động ESP-NOW
    if (esp_now_init() != ESP_OK) {

    }
    
    // Đăng ký hàm callback để xử lý dữ liệu nhận được
    esp_now_register_recv_cb(onDataRecv);

    // Đặt màu nền màn hình là màu đen
    StickCP2.Display.fillScreen(BLACK);

    StickCP2.Display.setRotation(3);

    StickCP2.Display.setTextSize(2);

    StickCP2.Display.fillScreen(BLACK);

    hienThiIntro();
}

void loop(){
    luaChonMode();
}
