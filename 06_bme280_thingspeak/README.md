# BME280 → ThingSpeak

## Wiring (I2C, same bus as the OLED)

| BME280 | Raspberry Pi |
|---|---|
| VIN | 3.3 V (pin 1) |
| GND | GND (pin 6) |
| SCL | GPIO3 (pin 5) |
| SDA | GPIO2 (pin 3) |

## ThingSpeak setup

1. Sign in at thingspeak.com and open Channels, then New Channel.
2. Tick Field 1 = Temperature, Field 2 = Humidity, Field 3 = Pressure, then Save.
3. Open the **API Keys** tab and copy the **Write API Key** into `THINGSPEAK_WRITE_KEY`.
4. The charts update live under Private View.

## Run

```bash
sudo raspi-config               # enable I2C
i2cdetect -y 1                  # should show 76 (or 77 -> change address in code)
pip3 install adafruit-blinka adafruit-circuitpython-bme280 requests
python3 bme280_read.py          # check the sensor first
python3 bme280_thingspeak.py
```

You can also test the upload without a sensor by pasting this into a browser:
`https://api.thingspeak.com/update?api_key=YOUR_KEY&field1=25`
It returns an entry number, or `0` if the update failed.

## Expected output

```
BME280 Initialized on Raspberry Pi I2C (0x76). Uploading to ThingSpeak...
[Reading #1] Temp: 28.41 C | Humidity: 56.20 % | Pressure: 948.37 hPa | Altitude: 549.12 m
 -> Uploaded to ThingSpeak (Entry ID: 1)
```

## Viva points

- The BME280 is a Bosch sensor that measures temperature, humidity and pressure. It speaks I2C (0x76 or 0x77) or SPI. The BMP280 is the cheaper version without humidity.
- ThingSpeak is a MathWorks IoT cloud. It has channels with up to 8 fields, a REST API (HTTP GET/POST `/update`), MQTT support and MATLAB analytics.
- The free tier allows one update every **15 s**. Anything faster returns `0`.
- The Write API key is for sending data and the Read API key is for fetching it (e.g. `/channels/<id>/feeds.json`).
