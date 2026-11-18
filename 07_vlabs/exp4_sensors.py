import time
import board
import busio
import digitalio
import adafruit_dht
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Exp 4: Ultrasonic (HC-SR04), PIR, DHT11/22, soil moisture, MQ135
# Soil moisture + MQ135 are analog -> MCP3008 CH0 / CH1 (same wiring as exp1)
# HC-SR04 ECHO is 5 V: use a 1k / 2k voltage divider into GPIO25

TRIG, ECHO = 24, 25
PIR_PIN = 17
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

dht = adafruit_dht.DHT11(board.D4)     # use adafruit_dht.DHT22 if that's the module

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
mcp = MCP.MCP3008(spi, digitalio.DigitalInOut(board.D5))
soil = AnalogIn(mcp, MCP.P0)
mq135 = AnalogIn(mcp, MCP.P1)


def distance_cm():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)                 # 10 us trigger pulse
    GPIO.output(TRIG, False)
    start = stop = time.time()
    timeout = start + 0.04
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        stop = time.time()
    return (stop - start) * 34300 / 2   # speed of sound 343 m/s, round trip


print("Multi-Sensor Demo Started on Raspberry Pi...")

try:
    while True:
        dist = distance_cm()
        motion = GPIO.input(PIR_PIN) == GPIO.HIGH
        GPIO.output(LED_PIN, motion)

        try:
            temp, hum = dht.temperature, dht.humidity
        except RuntimeError:            # DHT reads fail now and then - normal
            temp = hum = None

        soil_pct = round(100 - soil.value / 65535 * 100)   # dry = high reading (calibrate)
        air_raw = mq135.value >> 6                          # 0-1023

        print(f"Dist: {dist:.1f} cm | Motion: {'YES' if motion else 'NO'} | "
              f"Temp: {temp} C | Hum: {hum} % | Soil: {soil_pct} % | Air(MQ135): {air_raw}")
        time.sleep(2)
except KeyboardInterrupt:
    dht.exit()
    GPIO.cleanup()
    print("Stopped.")
