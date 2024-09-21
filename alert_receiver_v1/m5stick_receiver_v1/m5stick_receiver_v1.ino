//CHƯƠNG TRÌNH TẠO GIAO DIỆN NGƯỜI DÙNG ĐƠN GIẢN CHO ESP32 dựa trên một số hàm có sẵn của M5Stack
//CÓ THỂ DÙNG CHO NHIỀU DỰ ÁN
//DỰ ÁN ĐANG TEST: YOLO WATCHDOG

#include "M5StickCPlus2.h"  // Đọc tài liệu để cài thư viện M5StickC Plus 2
#include <esp_now.h>
#include <WiFi.h>

uint32_t duration_a = 100;

int g = 0;
int h = 0;
int i = 0;
int k = 0;

int x = 0;
int y = 0;
int z = 0;
int w = 0;
int num_a = 0;
int num_b = -1;
int num_c = 0;
char khuVuc1Cam = 'k';
char khuVuc2Cam = 'k';
char khuVuc3Cam = 'k';
char khuVuc4Cam = 'k';

typedef struct struct_message {
  int number_1;
  int number_2;
  int number_3;
  int number_4;
} struct_message;

// Khởi tạo cấu trúc dữ liệu
struct_message incomingData;

int count_a = 0;

// Hàm callback khi nhận được dữ liệu
void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
   
  if(incomingData.number_1 > 0 || incomingData.number_2 >0 || incomingData.number_3 >0 || incomingData.number_4 >0){
    StickCP2.Speaker.tone(4000, duration_a);
    g = incomingData.number_1;
    h = incomingData.number_2;
    i = incomingData.number_3;
    k = incomingData.number_4;
  }
}

void hienThiXacNhan(char y){
  if(y == 'a'){
    StickCP2.Display.print("khong nguoi");
  }
  if(y == 'b'){
    StickCP2.Display.print("coming soon");
  }
}

void hienThiDoiTuongCam(char n){
  if(n == 'a'){
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.setCursor(70, 70);
    StickCP2.Display.print("Co nguoi");
  }
  if(n == 'b'){
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.setCursor(70, 70);
    StickCP2.Display.print("Coming soon");
  }
}

void test_a(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(40, 40);
    StickCP2.Display.print("BI CAM:");

    int num_u = num_c % 2;

    if(num_u == 1){
      khuVuc1Cam = 'a';
    }
    if(num_u == 0){
      khuVuc1Cam = 'b';
    }

    hienThiDoiTuongCam(khuVuc1Cam);
    
    x++;
  }
}

void test_b(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(40, 40);
    StickCP2.Display.print("BI CAM:");

    int num_u = num_c % 2;

    if(num_u == 1){
      khuVuc2Cam = 'a';
    }
    if(num_u == 0){
      khuVuc2Cam = 'b';
    }

    hienThiDoiTuongCam(khuVuc2Cam);
    
    x++;
  }
}

void test_c(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(40, 40);
    StickCP2.Display.print("BI CAM:");

    int num_u = num_c % 2;

    if(num_u == 1){
      khuVuc3Cam = 'a';
    }
    if(num_u == 0){
      khuVuc3Cam = 'b';
    }

    hienThiDoiTuongCam(khuVuc3Cam);
    
    x++;
  }
}

void test_d(){
  if(x == 0){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.setCursor(40, 40);
    StickCP2.Display.print("BI CAM:");

    int num_u = num_c % 2;

    if(num_u == 1){
      khuVuc4Cam = 'a';
    }
    if(num_u == 0){
      khuVuc4Cam = 'b';
    }

    hienThiDoiTuongCam(khuVuc4Cam);
    
    x++;
  }
}

void enterViewMode(){
  if(num_c > 0){
     StickCP2.Display.clear();
      StickCP2.Display.setCursor(20, 20);
      StickCP2.Display.setTextColor(GREEN);
      StickCP2.Display.print("ONLINE");

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
  if(var_a == 1){
    StickCP2.Display.clear();
    StickCP2.Display.setTextColor(BLACK);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 13, 235, 20 , GREEN); //vẽ hình dạng fill hình có màu

    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("Khu vuc 1");
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.print("   Setup");

    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 4");    
  }

  if(var_a == 2){
    StickCP2.Display.clear();
    
    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.setTextColor(BLACK);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 43, 235, 20, GREEN); //vẽ hình dạng fill hình có màu

    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 2");
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.print("   Setup");

    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 4");      
  }

  if(var_a == 3){
    StickCP2.Display.clear();
    
    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setTextColor(BLACK);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 73, 235, 20, GREEN); //vẽ hình dạng fill hình có màu

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 3");
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.print("   Setup");
    
    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 4");     
  }

  if(var_a == 4){
    StickCP2.Display.clear();
    
    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("Khu vuc 1");

    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.setTextColor(BLACK);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 103, 235, 20, GREEN); //vẽ hình dạng fill hình có màu

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Khu vuc 4");
    StickCP2.Display.setTextColor(WHITE);
    StickCP2.Display.print("   Setup");
    
  }

  if(var_a == 5){
    StickCP2.Display.clear();
    
    StickCP2.Display.setTextColor(GREEN);

    StickCP2.Display.setCursor(20, 15);
    StickCP2.Display.print("Khu vuc 2");

    StickCP2.Display.setCursor(20, 45);
    StickCP2.Display.print("Khu vuc 3");

    StickCP2.Display.setCursor(20, 75);
    StickCP2.Display.print("Khu vuc 4");

    StickCP2.Display.setTextColor(BLACK);
    //StickCP2.Display.drawRect(5, 0, 235, 135, uiColor); //vẽ hình dạng viền
    StickCP2.Display.fillRect(5, 103, 235, 20, GREEN); //vẽ hình dạng fill hình có màu

    StickCP2.Display.setCursor(20, 105);
    StickCP2.Display.print("Xac nhan");
    
  }

}

void luaChonMode(){
  StickCP2.update();
  if(StickCP2.BtnA.wasClicked()){
    num_a++;
    num_c = 0;
    y = 0;
    x = 0;
    z = 0;
    w = 0;
  }

  if(num_a == 5){
    num_a = 0;
  }

  if(StickCP2.BtnB.wasClicked()){
    num_c++;
    x = 0;
    y = 0;
    z = 0;
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
      test_a();
    }
  }

  if(num_a == 1){
    if(num_c > 0){
      test_b();
    }
  }

  if(num_a == 2){
    if(num_c > 0){
      test_c();
    }
  }

  if(num_a == 3){
    if(num_c > 0){
      test_d();
    }
  }

  if(num_a == 4){
    if(num_c > 0){
      enterViewMode();
    }
  }
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

}

void loop() {
    luaChonMode();

}
