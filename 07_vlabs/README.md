# Virtual Labs (vlabs) questions

I don't have the exact vlab your syllabus refers to. These are the two official IoT Virtual Labs lists, with code for each experiment.

## A. iot-dei.vlabs.ac.in (Arduino / ESP32 simulation, Wokwi-style)

| # | Experiment | File |
|---|---|---|
| 1 | Input components: pushbutton, potentiometer, slider switch, photoresistor | `arduino_esp32/exp1_input_components.ino` |
| 2 | Output components: RGB LED, 7-segment, OLED, LCD 16×2, buzzer | `arduino_esp32/exp2_output_components.ino` |
| 3 | Motors: DC, servo, stepper | `arduino_esp32/exp3_motors.ino` |
| 4 | Sensors: ultrasonic, PIR, DHT, soil moisture, MQ135 | `arduino_esp32/exp4_sensors.ino` |
| 5 | Live data to an IoT platform over HTTP (ESP32 → ThingSpeak) | `arduino_esp32/exp5_esp32_http_thingspeak.ino` |
| 6 | Live data over MQTT (ESP32 → Mosquitto) | `arduino_esp32/exp6_esp32_mqtt.ino` |

To practise before the exam, open **wokwi.com**, start a new Arduino Uno or ESP32 project, paste the code, add the parts from the `+` menu, and wire them to the pins listed at the top of each file.
In Wokwi, the ESP32 Wi-Fi SSID is `Wokwi-GUEST` with an empty password.

## B. iot-amrt.vlabs.ac.in (Raspberry Pi)

| # | Experiment | Where |
|---|---|---|
| 1 | Introduction to Raspberry Pi | Theory, see below |
| 2 | LED blink | `raspberry_pi/rpi_vlab_programs.py led` |
| 3 | Push button + LED | `... button` |
| 4 | DHT11 | `... dht` |
| 5 | Ultrasonic sensor | `... ultrasonic` |
| 6 | Motor control with relay | `... relay` |
| 7 | Bluetooth data transfer to a smartphone | `../02_bluetooth/` |

### Raspberry Pi intro (viva)

- The Pi is a single-board computer with an ARM Cortex-A SoC (Pi 4 uses the BCM2711), runs Raspberry Pi OS (Linux), and has a 40-pin GPIO header.
- GPIO is **3.3 V logic and not 5 V tolerant**. It has **no built-in ADC**, so analog sensors need an MCP3008.
- It supports I2C (GPIO2/3), SPI (GPIO10/9/11), UART (GPIO14/15) and PWM (GPIO12/13/18/19).
- **BCM vs BOARD numbering**: `GPIO.setmode(GPIO.BCM)` uses GPIO numbers, while `GPIO.BOARD` uses physical pin numbers.
- **Pi vs Arduino**: the Pi is a microprocessor board running a full OS with multitasking and networking. The Arduino is a microcontroller (ATmega328P, 16 MHz) with no OS, runs in real time, and has an ADC.
