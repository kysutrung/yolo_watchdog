//TFT ST7798
//GPIO 14 ->SCK
//GPIO 13 ->SDA
//GPIO 4  ->RES
//GPIO 21 ->DC
//3.3V    ->BLK
#include <TFT_eSPI.h>  // Thư viện TFT_eSPI
TFT_eSPI tft = TFT_eSPI();  // Khởi tạo đối tượng TFT

//BUTTON
const int butA = 32;
const int butB = 33;
const int butC = 25;

//BUZZER
const int buzzerPin = 15;

//GLOBAL VAR
int meo = 0;
int lastMeo = 0;

//FUNCTION
void beepThreeTimes() {
  for(int i = 0; i < 3; i++) {
    tone(buzzerPin, 700, 100); // Phát âm thanh tần số 700 Hz trong 100 ms
    delay(200);                // Chờ đủ thời gian để âm thanh kêu và dừng lại
  }
}

void xinChao(){
  tft.fillScreen(TFT_WHITE);
  tft.setTextColor(TFT_BLACK);  // Màu chữ trắng
  tft.setTextSize(2);  // Kích thước chữ
  // Hiển thị chữ "Hello"
  tft.setCursor(50, 100);  // Đặt vị trí con trỏ (x, y)
  tft.print("Hello ");
  tft.print(meo);
}

//MAIN
void setup() {
  pinMode(butA, INPUT_PULLUP);
  pinMode(butB, INPUT_PULLUP);
  pinMode(butC, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);

  tft.init();  // Khởi tạo màn hình
  tft.setRotation(1);  // Đặt hướng màn hình (0, 90, 180, 270)
  tft.fillScreen(TFT_WHITE);  // Màu nền đen
  

}

void loop(){
  int x = digitalRead(butA);
  int y = digitalRead(butB);
  int z = digitalRead(butC);

  if(x == 0 || y == 0 || z == 0){
    tone(buzzerPin, 500, 10);
    meo++;
  }

  if(lastMeo != meo){
    xinChao();
    lastMeo = meo;
  }


  delay(10);
}