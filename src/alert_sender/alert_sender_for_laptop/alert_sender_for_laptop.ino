#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>

#define LED_PIN 4

uint8_t receiverMAC[] = {0xE4, 0x65, 0xB8, 0x78, 0x6A, 0x50};

typedef struct {
    int numbers[8];
} DataPacket;

DataPacket packet;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {

}


void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    if (esp_now_init() != ESP_OK) {
    }

    esp_now_register_send_cb(OnDataSent);

    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, receiverMAC, 6);
    peerInfo.channel = 0;  
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    }
}

void loop() {
    if (Serial.available() >= 32) {  //Mỗi int32 = 4 byte, 8 số = 32 byte
        int numbers[8];
        Serial.readBytes((char*)numbers, 32);

        for (int i = 0; i < 8; i++) {
            packet.numbers[i] = numbers[i];
        }

        esp_err_t result = esp_now_send(receiverMAC, (uint8_t*)&packet, sizeof(packet));

    }
}

