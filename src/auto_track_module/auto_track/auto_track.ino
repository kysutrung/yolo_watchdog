#include <ESP32Servo.h>

Servo myservo1;
Servo myservo2;
int servoPin1 = 13;
int servoPin2 = 12;

void setup() {
  Serial.begin(9600);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  myservo1.setPeriodHertz(50);
  myservo2.setPeriodHertz(50);

  myservo1.attach(servoPin1, 500, 2400);
  myservo2.attach(servoPin2, 500, 2400);

  myservo1.write(90);
  myservo2.write(90);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int sepIndex = data.indexOf(':');
    if (sepIndex > 0) {
      int servoID = data.substring(0, sepIndex).toInt();
      int angle = data.substring(sepIndex + 1).toInt();
      angle = constrain(angle, 0, 180);

      if (servoID == 1) {
        myservo1.write(angle);
      } else if (servoID == 2) {
        myservo2.write(angle);
      }
    }
  }
}
