"""
Raspberry Pi Virtual Lab programs (iot-amrt.vlabs.ac.in list), all in one file.
Run one:  python3 rpi_basic_programs.py led | button | dht | ultrasonic | relay
Wiring (BCM): LED=18, BUTTON=23 (to GND, pull-up), DHT11=4, TRIG=24, ECHO=25 (via divider), RELAY=17
"""
import sys
import time
import RPi.GPIO as GPIO

LED, BUTTON, DHT_PIN, TRIG, ECHO, RELAY = 18, 23, 4, 24, 25, 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def led_blink():
    GPIO.setup(LED, GPIO.OUT)
    while True:
        GPIO.output(LED, GPIO.HIGH); print("LED ON");  time.sleep(1)
        GPIO.output(LED, GPIO.LOW);  print("LED OFF"); time.sleep(1)


def button_led():
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        pressed = GPIO.input(BUTTON) == GPIO.LOW
        GPIO.output(LED, pressed)
        print("Button PRESSED -> LED ON" if pressed else "Button RELEASED -> LED OFF")
        time.sleep(0.2)


def dht11():
    # pip3 install adafruit-circuitpython-dht ; sudo apt install libgpiod2
    import board
    import adafruit_dht
    sensor = adafruit_dht.DHT11(board.D4)
    while True:
        try:
            print("Temp: {} C | Humidity: {} %".format(sensor.temperature, sensor.humidity))
        except RuntimeError as e:      # DHT reads fail often - just retry
            print("Retry: {}".format(e))
        time.sleep(2)


def ultrasonic():
    # ECHO is 5 V -> use 1k/2k voltage divider into the Pi
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    while True:
        GPIO.output(TRIG, False); time.sleep(0.05)
        GPIO.output(TRIG, True);  time.sleep(0.00001)
        GPIO.output(TRIG, False)
        start = end = time.time()
        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            end = time.time()
        distance = (end - start) * 34300 / 2
        print("Distance: {:.1f} cm".format(distance))
        time.sleep(1)


def relay_motor():
    # Most relay modules are active-LOW
    GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.HIGH)
    while True:
        GPIO.output(RELAY, GPIO.LOW);  print("Relay ON  -> Motor RUNNING"); time.sleep(3)
        GPIO.output(RELAY, GPIO.HIGH); print("Relay OFF -> Motor STOPPED"); time.sleep(3)


PROGRAMS = {"led": led_blink, "button": button_led, "dht": dht11,
            "ultrasonic": ultrasonic, "relay": relay_motor}

if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else "led"
    try:
        PROGRAMS[choice]()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Stopped.")
