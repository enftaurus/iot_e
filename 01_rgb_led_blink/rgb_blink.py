import RPi.GPIO as GPIO
import time

# Common-cathode RGB LED: R, G, B legs -> 220 ohm -> GPIO, longest leg -> GND
RED_PIN = 17     # physical pin 11
GREEN_PIN = 27   # physical pin 13
BLUE_PIN = 22    # physical pin 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in (RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# (name, R, G, B) - 1 = ON, 0 = OFF
COLORS = [
    ("RED",     1, 0, 0),
    ("GREEN",   0, 1, 0),
    ("BLUE",    0, 0, 1),
    ("YELLOW",  1, 1, 0),
    ("CYAN",    0, 1, 1),
    ("MAGENTA", 1, 0, 1),
    ("WHITE",   1, 1, 1),
]


def set_color(r, g, b):
    GPIO.output(RED_PIN, r)
    GPIO.output(GREEN_PIN, g)
    GPIO.output(BLUE_PIN, b)


print("RGB LED Blink Program Started on Raspberry Pi...")

try:
    while True:
        for name, r, g, b in COLORS:
            set_color(r, g, b)
            print(f"LED Color -> {name}")
            time.sleep(1)
            set_color(0, 0, 0)
            print("LED -> OFF")
            time.sleep(0.5)
except KeyboardInterrupt:
    set_color(0, 0, 0)
    GPIO.cleanup()
    print("RGB LED program stopped.")
