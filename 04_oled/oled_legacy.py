import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# For old Raspberry Pi OS (Python 2.7 / 3.5) where "import board" fails.
# Install: sudo pip3 install Adafruit-SSD1306   (also pulls Adafruit-GPIO)
oled = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
oled.begin()
oled.clear()
oled.display()
print("SSD1306 128x64 OLED Initialized on Raspberry Pi I2C (0x3C)")

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
cycle = 0

try:
    while True:
        cycle += 1
        temp_c = round(27.4 + (cycle % 5) * 0.3, 1)
        humidity = 55 + (cycle % 4)

        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        draw.rectangle((0, 0, 127, 63), outline=255, fill=0)
        draw.text((16, 4), "IOT ENV MONITOR", font=font, fill=255)
        draw.line((0, 16, 127, 16), fill=255)
        draw.text((8, 22), "Temp : {:.1f} C".format(temp_c), font=font, fill=255)
        draw.text((8, 35), "Humid: {} %".format(humidity), font=font, fill=255)
        draw.text((8, 49), "Node : ONLINE #{}".format(cycle), font=font, fill=255)

        oled.image(image)
        oled.display()

        print("OLED Frame #{} | Temp: {:.1f} C | Humidity: {} %".format(cycle, temp_c, humidity))
        time.sleep(2)
except KeyboardInterrupt:
    oled.clear()
    oled.display()
