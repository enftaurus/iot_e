import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from RPLCD.i2c import CharLCD

# Exp 2: Output components - RGB LED, 7-segment, OLED, LCD 16x2 (I2C), buzzer
# OLED (0x3C) and LCD backpack (0x27) share the I2C bus: SDA=GPIO2, SCL=GPIO3

RGB = {"R": 17, "G": 27, "B": 22}
BUZZER_PIN = 26                                  # active buzzer
SEG_PINS = [5, 6, 13, 19, 12, 16, 20]            # segments a..g (common cathode, 220 ohm each)
DIGITS = [                                       # a b c d e f g
    (1, 1, 1, 1, 1, 1, 0), (0, 1, 1, 0, 0, 0, 0), (1, 1, 0, 1, 1, 0, 1),
    (1, 1, 1, 1, 0, 0, 1), (0, 1, 1, 0, 0, 1, 1), (1, 0, 1, 1, 0, 1, 1),
    (1, 0, 1, 1, 1, 1, 1), (1, 1, 1, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0, 1, 1),
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(list(RGB.values()) + SEG_PINS + [BUZZER_PIN], GPIO.OUT, initial=GPIO.LOW)

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

lcd = CharLCD("PCF8574", 0x27, cols=16, rows=2)
lcd.clear()


def set_rgb(color):
    for name, pin in RGB.items():
        GPIO.output(pin, name == color)


def show_digit(n):
    for pin, state in zip(SEG_PINS, DIGITS[n]):
        GPIO.output(pin, state)


def beep(sec=0.15):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(sec)
    GPIO.output(BUZZER_PIN, GPIO.LOW)


print("Output Components Demo Started on Raspberry Pi...")

try:
    while True:
        for n in range(10):
            color = "RGB"[n % 3]
            set_rgb(color)
            show_digit(n)

            draw.rectangle((0, 0, oled.width, oled.height), fill=0)
            draw.text((0, 0), "IoT VLab Output", font=font, fill=255)
            draw.text((0, 20), f"Count: {n}", font=font, fill=255)
            draw.text((0, 36), f"RGB  : {color}", font=font, fill=255)
            oled.image(image)
            oled.show()

            lcd.cursor_pos = (0, 0)
            lcd.write_string("Hello IoT Lab")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"Count: {n}      ")

            beep()
            print(f"Count = {n} | RGB = {color} | 7-seg = {n}")
            time.sleep(0.85)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    lcd.clear()
    GPIO.cleanup()
    print("Stopped.")
