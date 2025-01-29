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
int lastGau = 0;
int lastTime = 0;
int count_a = 0;

//FUNCTION
void beepThreeTimes() {
  for(int i = 0; i < 3; i++) {
    tone(buzzerPin, 700, 100); // Phát âm thanh tần số 700 Hz trong 100 ms
    delay(200);                // Chờ đủ thời gian để âm thanh kêu và dừng lại
  }
}

void xinChao(){
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE);  // Màu chữ
  tft.setTextSize(3);  // Kích thước chữ
  // Hiển thị chữ "Hello"
  tft.setCursor(50, 40);
  tft.println("TESTING");
  tft.setCursor(50, 65);
  tft.println("PROGRAM");

  tft.setCursor(50, 120);
  tft.setTextColor(TFT_RED);  // Màu chữ


  tft.print(String(count_a));
  tft.print(" sec");

  tft.setTextColor(TFT_GREEN);  // Màu chữ
  tft.setCursor(40, 180);
  if(meo == 1){
    tft.print("Button 01");
  }
  if(meo == 2){
    tft.print("Button 02");
  }
  if(meo == 3){
    tft.print("Button 03");
  }
}

//MAIN
void setup() {
  pinMode(butA, INPUT_PULLUP);
  pinMode(butB, INPUT_PULLUP);
  pinMode(butC, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);

  tft.init();  // Khởi tạo màn hình
  tft.setRotation(0);  // Đặt hướng màn hình (0, 90, 180, 270)
  tft.fillScreen(TFT_WHITE);  // Màu nền đen
  

}

void loop(){
  int x = digitalRead(butA);
  int y = digitalRead(butB);
  int z = digitalRead(butC);

  unsigned long currentMillis = millis();
  if(currentMillis - lastTime >= 1000){
    count_a++;
    lastTime = currentMillis;
  }

  if(x == 0){
    tone(buzzerPin, 500, 10);
    meo = 1;
  }
  if(y == 0){
    tone(buzzerPin, 500, 10);
    meo = 2;
  }
  if(z == 0){
    tone(buzzerPin, 500, 10);
    meo = 3;
  }  

  if(lastMeo != count_a || lastGau != meo){
    xinChao();
    lastMeo = count_a;
    lastGau = meo;
  }


  delay(10);
}