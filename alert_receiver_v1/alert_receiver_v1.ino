//CODE cho esp32 nhận thông báo từ now

/*
CÁC NỘI DUNG ĐIỀU KHIỂN
  now - nhận data, xác nhận data đầy đủ - ok
  màn hình - chế độ cài đặt, chế độ nhận tin - ok, chế độ cảnh báo - ok
  nút A - nút mode chuyển giữa các chế độ và các ô
  nút B - nút cài đặt cấu hình, xác nhận cấu hình
  còi - kêu khi cảnh báo - ok
  led - đèn vàng báo now bị lỗi, đèn đỏ báo có cảnh báo ở chế độ tăt còi - hai đèn cháy chưa test
*/

#include <esp_now.h>
#include <WiFi.h>

//led
const int ledNow = 34;
const int ledWan = 35;

//còi
const int coiBeep = 27;

void beepThreeTimes() {
  for(int i = 0; i < 3; i++) {
    tone(coiBeep, 700, 100); // Phát âm thanh tần số 700 Hz trong 100 ms
    delay(200);                // Chờ đủ thời gian để âm thanh kêu và dừng lại
  }
}

//nut bam
//chua phat trien xong
//cần đáp 4 biến global ra ngoài xong mỗi lần nhận đc tín hiệu đến thì sửa
//thế thì mới làm được
const int but_a = 14;
const int but_b = 13;

// Cấu trúc dữ liệu để nhận
typedef struct struct_message {
  int number_1;
  int number_2;
  int number_3;
  int number_4;
} struct_message;

// Khởi tạo cấu trúc dữ liệu
struct_message incomingData;

//xử lý màn hình thông báo
#include <TFT_eSPI.h>  // Thư viện điều khiển màn hình TFT
#include <SPI.h>       // Thư viện giao tiếp SPI (phải khai báo chân ở trong file setup thư viện)

TFT_eSPI tft = TFT_eSPI();  // Khởi tạo đối tượng TFT_eSPI

int screenWidth = tft.width();   // Lấy chiều rộng của màn hình
int screenHeight = tft.height(); // Lấy chiều cao của màn hình
int line1_y = screenHeight / 4;
int line2_y = screenHeight / 2;
int line3_y = (screenHeight * 3) / 4;

int count_a = 0;

// Hàm callback khi nhận được dữ liệu
void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
  tft.setTextSize(2);        // Kích thước chữ
  if(count_a < 1){
    tft.fillScreen(TFT_BLACK); // Xóa màn hình, đặt nền màu đen
    count_a++;
  }
   
  if(incomingData.number_1 > 0 || incomingData.number_2 >0 || incomingData.number_3 >0 || incomingData.number_4 >0){
    beepThreeTimes();
    digitalWrite(ledWan, HIGH);
  }
  else{
    digitalWrite(ledWan, LOW);
  }

  if(incomingData.number_1 > 0){
    tft.setTextColor(TFT_RED, TFT_BLACK);
    tft.setCursor(20, 20);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV1: ");
    tft.print(incomingData.number_1);
    tft.print(" nguoi");
  }
  else{
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.setCursor(20, 20);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV1: ");
    tft.print("An toan");
  }

  if(incomingData.number_2 > 0){
    tft.setTextColor(TFT_RED, TFT_BLACK); 
    tft.setCursor(20, 80);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV2: ");
    tft.print(incomingData.number_2);
    tft.print(" nguoi");
  }
  else{
    tft.setTextColor(TFT_GREEN, TFT_BLACK); 
    tft.setCursor(20, 80);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV2: ");
    tft.print("An toan");
  }

  if(incomingData.number_3 > 0){
    tft.setTextColor(TFT_RED, TFT_BLACK);
    tft.setCursor(20, 140);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV3: ");
    tft.print(incomingData.number_3);
    tft.print(" nguoi");
  }
  else{
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.setCursor(20, 140);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV3: ");
    tft.print("An toan");
  }

  if(incomingData.number_4 > 0){
    tft.setTextColor(TFT_RED, TFT_BLACK); 
    tft.setCursor(20, 200);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV4: ");
    tft.print(incomingData.number_4);
    tft.print(" nguoi");
  }
  else{
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.setCursor(20, 200);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
    tft.print("KV4: ");
    tft.print("An toan");
  }

  tft.drawLine(0, line1_y, screenWidth, line1_y, TFT_WHITE);  // Đường ngang 1
  tft.drawLine(0, line2_y, screenWidth, line2_y, TFT_WHITE);  // Đường ngang 2
  tft.drawLine(0, line3_y, screenWidth, line3_y, TFT_WHITE);  // Đường ngang 3
  tft.drawRect(0, 0, screenWidth, screenHeight, TFT_WHITE);  // Vẽ viền
}

void setup() {
  //nut bấm
  pinMode(but_a, INPUT);
  pinMode(but_b, INPUT);
  //led báo
  pinMode(ledNow, OUTPUT);
  digitalWrite(ledNow, LOW);
  pinMode(ledWan, OUTPUT);
  //còi
  pinMode(coiBeep, OUTPUT);
  
  // Khởi động Wi-Fi ở chế độ Station (trạm)
  WiFi.mode(WIFI_STA);
  
  // Khởi động ESP-NOW
  if (esp_now_init() != ESP_OK) {
    digitalWrite(ledNow, HIGH);
  }
  
  // Đăng ký hàm callback để xử lý dữ liệu nhận được
  esp_now_register_recv_cb(onDataRecv);

  //man hinh
  tft.init();                // Khởi tạo màn hình TFT
  tft.setRotation(0);        // Đặt chiều xoay của màn hình (tùy thuộc vào chiều muốn chia)
  tft.fillScreen(TFT_BLACK); // Xóa màn hình, đặt nền màu đen
  tft.drawRect(0, 0, screenWidth, screenHeight, TFT_RED);  // Vẽ viền
  tft.setTextColor(TFT_RED, TFT_BLACK);
  tft.setTextSize(3);        // Kích thước chữ
  tft.setCursor(40, 105);    // Đặt vị trí chữ trên màn hình (tọa độ x, y)
  tft.print("NO SIGNAL");
}

void loop() {
}
