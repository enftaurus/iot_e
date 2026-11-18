# OLED (SSD1306, 128×64, I2C)

## Wiring

| OLED | Raspberry Pi |
|---|---|
| VCC | 3.3 V (pin 1) |
| GND | GND (pin 6) |
| SCL | GPIO3 / SCL (pin 5) |
| SDA | GPIO2 / SDA (pin 3) |

## Setup

```bash
sudo raspi-config               # Interface Options -> I2C -> Enable, then reboot
sudo apt install -y i2c-tools python3-pil
i2cdetect -y 1                  # should show 3c (some modules use 3d)
pip3 install adafruit-blinka adafruit-circuitpython-ssd1306
python3 oled_iot_monitor.py
```

On Raspberry Pi OS Bookworm, plain `pip3 install` is blocked. Either add `--break-system-packages` or use a venv: `python3 -m venv --system-site-packages env && source env/bin/activate`.

## Files

- `oled_iot_monitor.py` is the main program from the lab manual: a live dashboard with a border, header, temperature and humidity.
- `oled_hello.py` is a minimal "print text" version. Edit the name if needed.

## Viva points

- SSD1306 is the driver IC. The display is 128×64 monochrome and needs no backlight, because each OLED pixel emits its own light.
- I2C is a 2-wire bus (SDA = data, SCL = clock) where each device has a 7-bit address. Here it's 0x3C.
- PIL draws into an in-memory image. `oled.image()` copies it to the buffer and `oled.show()` pushes it over I2C.
