#include "M5StickCPlus2.h"  // Đọc tài liệu để cài thư viện M5StickC Plus 2

void setup() {
    // Cấu hình và khởi động M5StickC Plus 2
    auto cfg = M5.config();
    StickCP2.begin(cfg);

    // Đặt màu nền màn hình là màu đen
    StickCP2.Display.fillScreen(BLACK);

    StickCP2.Display.setRotation(1);

    StickCP2.Display.setTextSize(2);
    StickCP2.Display.setTextColor(GREEN);
    StickCP2.Display.setCursor(20, 10);
    StickCP2.Display.println("KV1: An Toan");
    StickCP2.Display.setCursor(20, 40);
    StickCP2.Display.println("KV2: An Toan");
    StickCP2.Display.setTextColor(RED);
    StickCP2.Display.setCursor(20, 70);
    StickCP2.Display.println("KV3: 2 Nguoi");
    StickCP2.Display.setTextColor(GREEN);
    StickCP2.Display.setCursor(20, 100);
    StickCP2.Display.println("KV4: An Toan");
}

void loop() {
    // Không làm gì trong loop
}
