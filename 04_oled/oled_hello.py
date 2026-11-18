import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Minimal version: if asked to "display your name / roll no on OLED"
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

draw.text((0, 0), "Hello IoT Lab!", font=font, fill=255)
draw.text((0, 16), "Name: Raja Babu", font=font, fill=255)
draw.text((0, 32), "VCE - CSE", font=font, fill=255)
draw.rectangle((0, 50, 127, 63), outline=255, fill=0)

oled.image(image)
oled.show()
print("Text displayed on OLED")
