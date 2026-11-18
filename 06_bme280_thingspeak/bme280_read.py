import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Sensor-only test: run this first to confirm wiring before ThingSpeak.
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

try:
    while True:
        print("Temp: {:.2f} C | ".format(bme280.temperature) +
              "Humidity: {:.2f} % | ".format(bme280.relative_humidity) +
              "Pressure: {:.2f} hPa".format(bme280.pressure))
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped.")
