# IoT Lab Exam – Programs & Notes

Raspberry Pi (Python) programs for every topic in the lab exam syllabus, written in the same style as the lab manual. There are also Arduino/ESP32 versions for the vlabs questions.

| # | Topic | Folder | Main file |
|---|---|---|---|
| 1 | Blink RGB LED | `01_rgb_led_blink/` | `rgb_blink.py` (+ `rgb_pwm_fade.py`) |
| 2 | Bluetooth | `02_bluetooth/` | `bt_led_server.py` |
| 3 | MQTT (Mosquitto + Adafruit IO) | `03_mqtt/` | `mqtt_publisher.py`, `mqtt_subscriber.py`, `adafruit_io_mqtt.py` |
| 4 | OLED SSD1306 | `04_oled/` | `oled_iot_monitor.py` |
| 5 | Zigbee (XBee) | `05_zigbee/` | `zigbee_coordinator.py`, `zigbee_router.py`, **`THEORY.md`** |
| 6 | BME280 → ThingSpeak | `06_bme280_thingspeak/` | `bme280_thingspeak.py` |
| 7 | vlabs questions | `07_vlabs/` | Arduino/ESP32 `.ino` + Pi programs |

Each folder has a README covering wiring, setup commands, expected output and viva points.

## Quick setup on the Pi

```bash
sudo raspi-config        # Interface Options: enable I2C, Serial Port (no login shell), reboot
sudo apt update && sudo apt install -y i2c-tools python3-pip mosquitto-clients bluetooth bluez
pip3 install -r requirements.txt        # Bookworm: add --break-system-packages, or use a venv
i2cdetect -y 1                          # OLED = 3c, BME280 = 76/77
```

## Pin cheat sheet (BCM numbering)

| Use | GPIO | Physical pin |
|---|---|---|
| 3.3 V / 5 V / GND | – | 1 / 2 / 6 |
| I2C SDA / SCL (OLED, BME280) | 2 / 3 | 3 / 5 |
| UART TX / RX (XBee) | 14 / 15 | 8 / 10 |
| LED (Bluetooth, MQTT, Zigbee) | 18 | 12 |
| RGB R / G / B | 17 / 27 / 22 | 11 / 13 / 15 |

Always put a 220 Ω resistor in series with each LED.

## Libraries used

| Library | pip name | Used in |
|---|---|---|
| `RPi.GPIO` | `RPi.GPIO` (preinstalled) | LED, Bluetooth, MQTT, Zigbee |
| `serial` | `pyserial` | Zigbee |
| `board`, `busio` | `adafruit-blinka` | OLED, BME280 |
| `adafruit_ssd1306` | `adafruit-circuitpython-ssd1306` | OLED |
| `PIL` | `pillow` | OLED drawing |
| `adafruit_bme280` | `adafruit-circuitpython-bme280` | BME280 |
| `requests` | `requests` | ThingSpeak |
| `paho.mqtt` | `paho-mqtt` (v2) | MQTT |
| `Adafruit_IO` | `adafruit-io` | Adafruit IO MQTT |
| `socket` (AF_BLUETOOTH) | built-in | Bluetooth |
