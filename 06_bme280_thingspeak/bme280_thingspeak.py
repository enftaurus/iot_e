import time
import board
import busio
import requests
from adafruit_bme280 import basic as adafruit_bme280

# BME280 (temperature, humidity, pressure) -> ThingSpeak cloud channel
# ThingSpeak: create channel, enable Field1 = Temperature, Field2 = Humidity,
# Field3 = Pressure, then copy the Write API Key from "API Keys" tab.

THINGSPEAK_WRITE_KEY = "XXXXXXXXXXXXXXXX"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)   # try 0x77 if not found
bme280.sea_level_pressure = 1013.25

print("BME280 Initialized on Raspberry Pi I2C (0x76). Uploading to ThingSpeak...")

count = 0
try:
    while True:
        count += 1
        temperature = round(bme280.temperature, 2)
        humidity = round(bme280.relative_humidity, 2)
        pressure = round(bme280.pressure, 2)
        altitude = round(bme280.altitude, 2)

        print("[Reading #{}] Temp: {} C | Humidity: {} % | ".format(count, temperature, humidity) +
              "Pressure: {} hPa | Altitude: {} m".format(pressure, altitude))

        params = {
            "api_key": THINGSPEAK_WRITE_KEY,
            "field1": temperature,
            "field2": humidity,
            "field3": pressure,
        }
        try:
            r = requests.get(THINGSPEAK_URL, params=params, timeout=10)
            entry_id = r.text.strip()
            if entry_id != "0":
                print(" -> Uploaded to ThingSpeak (Entry ID: {})".format(entry_id))
            else:
                print(" -> Upload rejected (check API key / 15 s rate limit)")
        except requests.RequestException as e:
            print(" -> Network error: {}".format(e))

        time.sleep(20)   # free ThingSpeak accounts accept one update every 15 s
except KeyboardInterrupt:
    print("BME280 ThingSpeak upload stopped.")
