#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#define LED_PIN 4

// Địa chỉ MAC của hai thiết bị nhận
uint8_t receiverMACofPrototype2[] = {0xE4, 0x65, 0xB8, 0x78, 0x6A, 0x50};
uint8_t receiverMACofM5[] = {0x10, 0x06, 0x1C, 0x27, 0xEF, 0x14};

// Cấu trúc dữ liệu gửi đi
typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

// Callback khi gửi xong
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {

}

void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    
    if (esp_now_init() != ESP_OK) {
        return;
    }

    esp_now_register_send_cb(OnDataSent);

    // Thêm cả hai thiết bị nhận
    esp_now_peer_info_t peerInfo = {};

    // Thêm thiết bị receiverMACofM5
    memcpy(peerInfo.peer_addr, receiverMACofM5, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    }

    // Thêm thiết bị receiverMACofPrototype2
    memcpy(peerInfo.peer_addr, receiverMACofPrototype2, 6);
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    }
}

void loop() {
    if (Serial.available() >= 32) {  // Mỗi int32 = 4 byte, 8 số = 32 byte
        int numbers[8];
        Serial.readBytes((char*)numbers, 32);

        for (int i = 0; i < 8; i++) {
            packet.numbers[i] = numbers[i];
        }

        // Gửi dữ liệu đến cả hai thiết bị
        esp_err_t result1 = esp_now_send(receiverMACofM5, (uint8_t*)&packet, sizeof(packet));
        esp_err_t result2 = esp_now_send(receiverMACofPrototype2, (uint8_t*)&packet, sizeof(packet));

    }
}

//////////////////////////////////////////////////////////////////
// #include <esp_now.h>
// #include <WiFi.h>

// #define LED_PIN 4

// uint8_t receiverMACofPrototype2[] = {0xE4, 0x65, 0xB8, 0x78, 0x6A, 0x50};
// uint8_t receiverMACofM5[] = {0x10, 0x06, 0x1C, 0x27, 0xEF, 0x14};

// typedef struct {
//     int numbers[8];
// } DataPacket;

// DataPacket packet;

// void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {

// }


// void setup() {
//     Serial.begin(115200);
//     WiFi.mode(WIFI_STA);
//     if (esp_now_init() != ESP_OK) {
//     }

//     esp_now_register_send_cb(OnDataSent);

//     esp_now_peer_info_t peerInfo = {};
//     memcpy(peerInfo.peer_addr, receiverMACofM5, 6);
//     peerInfo.channel = 0;  
//     peerInfo.encrypt = false;

//     if (esp_now_add_peer(&peerInfo) != ESP_OK) {
//     }
// }

// void loop() {
//     if (Serial.available() >= 32) {  //Mỗi int32 = 4 byte, 8 số = 32 byte
//         int numbers[8];
//         Serial.readBytes((char*)numbers, 32);

//         for (int i = 0; i < 8; i++) {
//             packet.numbers[i] = numbers[i];
//         }

//         esp_err_t result = esp_now_send(receiverMACofM5, (uint8_t*)&packet, sizeof(packet));

//     }
// }
