# Virtual Labs (vlabs) questions: Raspberry Pi / Python

All programs here are Python for the Raspberry Pi. They cover the experiments from both official IoT Virtual Labs lists.

## A. iot-dei.vlabs.ac.in list

| # | Experiment | File |
|---|---|---|
| 1 | Inputs: pushbutton, slider switch, potentiometer, LDR | `exp1_input_components.py` |
| 2 | Outputs: RGB LED, 7-segment, OLED, LCD 16×2, buzzer | `exp2_output_components.py` |
| 3 | Motors: DC (L298N), servo, stepper | `exp3_motors.py` |
| 4 | Sensors: ultrasonic, PIR, DHT, soil moisture, MQ135 | `exp4_sensors.py` |
| 5 | Live data to an IoT platform over HTTP (ThingSpeak) | `exp5_http_thingspeak.py` |
| 6 | Live data over MQTT | `exp6_mqtt_sensor.py` |

## B. iot-amrt.vlabs.ac.in list

All of these are in `rpi_basic_programs.py`. Run one with `python3 rpi_basic_programs.py <name>`.

| Experiment | Name to pass |
|---|---|
| LED blink | `led` |
| Push button + LED | `button` |
| DHT11 | `dht` |
| Ultrasonic sensor | `ultrasonic` |
| Motor with relay | `relay` |
| Bluetooth to smartphone | see `../02_bluetooth/` |

## Extra libraries for this folder

```bash
pip3 install adafruit-circuitpython-mcp3xxx adafruit-circuitpython-dht RPLCD
sudo apt install -y libgpiod2         # needed by adafruit_dht
sudo raspi-config                     # enable SPI (for MCP3008) and I2C (OLED/LCD)
```

## Key point: the Pi has no ADC

The potentiometer, LDR, soil moisture sensor and MQ135 all give **analog** output. The Raspberry Pi can't read analog signals, so they go through an **MCP3008** (an 8-channel, 10-bit SPI ADC). Expect an examiner to ask about this.

| MCP3008 pin | Raspberry Pi |
|---|---|
| VDD, VREF | 3.3 V |
| AGND, DGND | GND |
| CLK | GPIO11 (SCLK) |
| DOUT | GPIO9 (MISO) |
| DIN | GPIO10 (MOSI) |
| CS/SHDN | GPIO5 |

## Raspberry Pi intro (viva)

- The Pi is a single-board computer with an ARM SoC (BCM2711 on the Pi 4). It runs Raspberry Pi OS (Linux) and has a 40-pin GPIO header.
- GPIO uses **3.3 V logic and is not 5 V tolerant**. That's why the HC-SR04 echo pin needs a voltage divider.
- Buses: I2C on GPIO2/3, SPI on GPIO10/9/11, UART on GPIO14/15. Hardware PWM is on GPIO12/13/18/19.
- `GPIO.BCM` uses GPIO numbers and `GPIO.BOARD` uses physical pin numbers.
- A servo needs a 50 Hz PWM signal with a 0.5–2.5 ms pulse (0–180°). A DC motor's speed comes from the PWM duty cycle on the driver's EN pin.
