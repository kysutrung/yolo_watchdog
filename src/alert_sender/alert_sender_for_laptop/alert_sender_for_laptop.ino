#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#define LED_PIN 4  // Chân GPIO4 để điều khiển LED

// Định nghĩa địa chỉ MAC broadcast
uint8_t receiverMAC[] = {0xE4, 0x65, 0xB8, 0x78, 0x6A, 0x50};

// Định nghĩa struct chứa 8 số nguyên
typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

// Hàm callback khi gửi dữ liệu
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    // Serial.print("Gửi dữ liệu: ");
    // Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Thành công" : "Thất bại");
}


void setup() {
    Serial.begin(115200);

    // Đặt ESP32 vào chế độ Wi-Fi Station
    WiFi.mode(WIFI_STA);

    // Khởi tạo ESP-NOW
    if (esp_now_init() != ESP_OK) {
        // Serial.println("Lỗi khi khởi tạo ESP-NOW");
        return;
    }
    // Serial.println("ESP-NOW đã khởi tạo!");

    // Đăng ký callback khi gửi dữ liệu
    esp_now_register_send_cb(OnDataSent);

    // Cấu hình broadcast peer
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, receiverMAC, 6);
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;

    // Thêm peer vào danh sách
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        // Serial.println("Lỗi khi thêm peer!");
        // return;
    }

    // Serial.println("ESP32 Sender đã sẵn sàng!");
}

void loop() {
    if (Serial.available() >= 32) {  // Mỗi int32 = 4 byte, 8 số = 32 byte
        int numbers[8];
        Serial.readBytes((char*)numbers, 32);  // Nhận dữ liệu vào mảng

        // Gán giá trị vào struct
        for (int i = 0; i < 8; i++) {
            packet.numbers[i] = numbers[i];
        }

        // Gửi dữ liệu qua ESP-NOW broadcast
        esp_err_t result = esp_now_send(receiverMAC, (uint8_t*)&packet, sizeof(packet));

        // if (result == ESP_OK) {
        //     Serial.println("Đã gửi dữ liệu!");
        // } else {
        //     Serial.println("Lỗi khi gửi dữ liệu!");
        // }

        // delay(100);  // Gửi mỗi giây

    }
}

