import time
import board
import busio
import digitalio
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Exp 1: Input components - pushbutton, slider switch (digital) +
#        potentiometer, photoresistor/LDR (analog via MCP3008 ADC, since the Pi has no ADC)
#
# MCP3008 -> Pi (SPI): VDD,VREF->3.3V | AGND,DGND->GND | CLK->GPIO11 | DOUT->GPIO9 (MISO)
#                      DIN->GPIO10 (MOSI) | CS->GPIO5
# Pot wiper -> CH0 ; LDR + 10k divider -> CH1

BUTTON_PIN = 23   # button to GND, internal pull-up
SLIDE_PIN = 24    # slider switch middle pin, other side to GND
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SLIDE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
pot = AnalogIn(mcp, MCP.P0)
ldr = AnalogIn(mcp, MCP.P1)

print("Input Components Demo Started on Raspberry Pi...")

try:
    while True:
        pressed = GPIO.input(BUTTON_PIN) == GPIO.LOW
        slide_on = GPIO.input(SLIDE_PIN) == GPIO.LOW
        GPIO.output(LED_PIN, pressed)

        pot_pct = round(pot.value / 65535 * 100)      # .value is 0-65535
        light = ldr.value >> 6                         # scale to 0-1023 like Arduino

        print("Button: {} | ".format('PRESSED' if pressed else 'RELEASED') +
              "Slide: {} | ".format('ON' if slide_on else 'OFF') +
              "Pot: {}% ({:.2f} V) | LDR: {}".format(pot_pct, pot.voltage, light))
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stopped.")
