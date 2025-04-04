#define USER_SETUP_INFO "User_Setup"

#define ST7789_DRIVER      // màn hình vuông trungtaulua


#define TFT_WIDTH  240 // ST7789 240 x 240 and 240 x 320

#define TFT_HEIGHT 240 // ST7789 240 x 240

//cho màn hình vuông
#define TFT_SCLK 14   
#define TFT_CS    5    
#define TFT_MOSI 13   // SDA
#define TFT_RST  4    // RES
#define TFT_DC   21   // DC

#define LOAD_GLCD   // Font 1. Original Adafruit 8 pixel font needs ~1820 bytes in FLASH
#define LOAD_FONT2  // Font 2. Small 16 pixel high font, needs ~3534 bytes in FLASH, 96 characters
#define LOAD_FONT4  // Font 4. Medium 26 pixel high font, needs ~5848 bytes in FLASH, 96 characters
#define LOAD_FONT6  // Font 6. Large 48 pixel font, needs ~2666 bytes in FLASH, only characters 1234567890:-.apm
#define LOAD_FONT7  // Font 7. 7 segment 48 pixel font, needs ~2438 bytes in FLASH, only characters 1234567890:-.
#define LOAD_FONT8  // Font 8. Large 75 pixel font needs ~3256 bytes in FLASH, only characters 1234567890:-.
//#define LOAD_FONT8N // Font 8. Alternative to Font 8 above, slightly narrower, so 3 digits fit a 160 pixel TFT
#define LOAD_GFXFF  // FreeFonts. Include access to the 48 Adafruit_GFX free fonts FF1 to FF48 and custom fonts
#define SMOOTH_FONT

#define SPI_FREQUENCY  27000000

#define SPI_READ_FREQUENCY  20000000

#define SPI_TOUCH_FREQUENCY  2500000
