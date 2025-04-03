#ifndef THEMENU_H
#define THEMENU_H

//LIBRARY
#include "M5StickCPlus2.h"
#include "yourPrograms.h"

//GLOBAL VAR
extern int MAIN_MENU_MODE;
extern int LAST_MAIN_MENU_MODE;
extern bool HAVE_ACCESS_THIS_MODE;

// Khai báo các hàm
void getButtonz();

void setMainMenu();

void setQuikMode();
void setProgramsMenu();
void setGeneralSettingMode();
void setAboutDisplay();

#endif