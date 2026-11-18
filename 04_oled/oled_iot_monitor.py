import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Initialize Raspberry Pi I2C bus and 128x64 SSD1306 OLED at 0x3C
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.show()
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

        # Clear framebuffer and draw IoT dashboard layout
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        draw.rectangle((0, 0, 127, 63), outline=255, fill=0)
        draw.text((16, 4), "IOT ENV MONITOR", font=font, fill=255)
        draw.line((0, 16, 127, 16), fill=255)

        draw.text((8, 22), f"Temp : {temp_c:.1f} C", font=font, fill=255)
        draw.text((8, 35), f"Humid: {humidity} %", font=font, fill=255)
        draw.text((8, 49), f"Node : ONLINE #{cycle}", font=font, fill=255)

        oled.image(image)
        oled.show()

        print(f"OLED Frame #{cycle} | Temp: {temp_c:.1f} C | Humidity: {humidity} %")
        time.sleep(2)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
