import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Sensor-only test: run this first to confirm wiring before ThingSpeak.
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

try:
    while True:
        print(f"Temp: {bme280.temperature:.2f} C | "
              f"Humidity: {bme280.relative_humidity:.2f} % | "
              f"Pressure: {bme280.pressure:.2f} hPa")
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopped.")
