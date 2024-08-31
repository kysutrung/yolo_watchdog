//nhận tín hiệu esp now
#include <esp_now.h>
#include <WiFi.h>
//đèn báo tín hiệu, đèn báo nguồn, đèn báo các trường hợp cảnh báo
#define ledNow 25
//còi báo động
#define beepPin 26
//xử lý màn hình thông báo
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET     -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Cấu trúc dữ liệu để nhận
struct duLieu {
  int a;
  int b;
  int c;
  int d;
};

// Khởi tạo cấu trúc dữ liệu
duLieu duLieuDieuKhien;

// Hàm callback khi nhận được dữ liệu
void xuLyDuLieuNhan(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&duLieuDieuKhien, data, sizeof(duLieuDieuKhien));

  Serial.print("Received: ");
  Serial.println(duLieuDieuKhien.a);
  Serial.println(duLieuDieuKhien.b);
  Serial.println(duLieuDieuKhien.c);
  Serial.println(duLieuDieuKhien.d);

  int num_a = duLieuDieuKhien.a;
  int num_b = duLieuDieuKhien.b;
  int num_c = duLieuDieuKhien.c`;
  int num_d = duLieuDieuKhien.d;

  if(num_a != 0 || num_b != 0 || num_c != 0 || num_d != 0){
    tone(beepPin, 700, 200);
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print("KV1: ");
    display.print(num_a);
    display.print(" nguoi");
    display.setCursor(0, 10);
    display.print("KV2: ");
    display.print(num_b);
    display.print(" nguoi");
    display.setCursor(0, 20);
    display.print("KV3: ");
    display.print(num_c);
    display.print(" nguoi");
    display.setCursor(0, 30);
    display.print("KV4: ");
    display.print(num_d);
    display.print(" nguoi");
    display.display();
  }
  else{
    display.clearDisplay();
  }
}

void setup() {
  // Khởi động Serial Monitor
  Serial.begin(115200);
  // LED
  pinMode(ledNow, OUTPUT);
  digitalWrite(ledNow, HIGH);
  // Còi
  pinMode(beepPin, OUTPUT);
  
  // Khởi động Wi-Fi ở chế độ Station (trạm)
  WiFi.mode(WIFI_STA);
  
  // Khởi động ESP-NOW
  if (esp_now_init() != ESP_OK) {
    digitalWrite(ledNow, LOW);
  }
  
  //Màn hình
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("Không thể tìm thấy màn hình OLED"));
    for(;;);
  }

  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  // Đăng ký hàm để xử lý dữ liệu nhận được
  esp_now_register_recv_cb(xuLyDuLieuNhan);
  
  Serial.println("ESP-NOW Receiver Initialized");
}

void loop() {
  //chẳng làm cc gì ở đây cả nhưng vẫn phải viết ra cho đủ
}
