import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Thiết lập I2C và SSD1306
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Xóa màn hình
oled.fill(0)
oled.show()

# Tạo hình ảnh trống với kích thước màn hình OLED
image = Image.new("1", (oled.width, oled.height))

# Lấy đối tượng vẽ
draw = ImageDraw.Draw(image)

# Tạo font chữ (sử dụng font mặc định)
font = ImageFont.load_default()

# Viết chữ "Hello World" lên màn hình
text = "dit me may"
(draw_width, draw_height) = draw.textsize(text, font=font)
draw.text(((oled.width - draw_width) // 2, (oled.height - draw_height) // 2), text, font=font, fill=255)

# Hiển thị hình ảnh trên màn hình OLED
oled.image(image)
oled.show()
