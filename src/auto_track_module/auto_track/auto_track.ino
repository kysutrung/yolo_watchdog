#include<ESP32Servo.h>

Servo myservo1;
Servo myservo2;
int servoPin1 = 13;
int servoPin2 = 12;

int cLocX = 0;
int nLocX = 0;
int cLocY = 0;
int nLocY = 0;

void setup() {
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
  delay(2000);
}

void moveServo(Servo &servo, int gocA, int gocB, int speed) {
  if (gocA < gocB) {
    for (int vitri = gocA; vitri <= gocB; vitri++) {
      servo.write(vitri);
      delay(speed);
    }
  } else {
    for (int vitri = gocA; vitri >= gocB; vitri--) {
      servo.write(vitri);
      delay(speed);
    }
  }
}

void loop() {
  moveServo(myservo1, 0, 170, 30);
  moveServo(myservo1, 170, 0, 30);
}