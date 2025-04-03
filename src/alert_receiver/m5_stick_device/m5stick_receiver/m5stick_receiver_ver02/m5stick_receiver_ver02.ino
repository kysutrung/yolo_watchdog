#include "theMenu.h"

void setup() {
  auto cfg = M5.config();
  StickCP2.begin(cfg);

  StickCP2.Display.setRotation(1);
  StickCP2.Display.setTextColor(WHITE);
  StickCP2.Display.setTextFont(&fonts::FreeSerif9pt7b);

}

void loop() {
  setMainMenu();
}
