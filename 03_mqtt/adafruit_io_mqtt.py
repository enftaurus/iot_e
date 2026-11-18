import time
import random
import RPi.GPIO as GPIO
from Adafruit_IO import MQTTClient

# MQTT with Adafruit IO (io.adafruit.com) as the cloud broker + dashboard.
# 1. Create a free account at io.adafruit.com
# 2. Create two feeds: "temperature" and "led"
# 3. Dashboard: add a Gauge/Line chart on "temperature" and a Toggle (ON/OFF) on "led"
# 4. Copy Username + Active Key from the yellow key icon

ADAFRUIT_IO_USERNAME = "your_username"
ADAFRUIT_IO_KEY = "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

FEED_TEMP = "temperature"
FEED_LED = "led"

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)


def connected(client):
    print("Connected to Adafruit IO MQTT broker (io.adafruit.com:1883)")
    client.subscribe(FEED_LED)
    print(f"Subscribed to feed: {FEED_LED}")


def disconnected(client):
    print("Disconnected from Adafruit IO")


def message(client, feed_id, payload):
    print(f"[SUB] Feed {feed_id} -> {payload}")
    if feed_id == FEED_LED:
        GPIO.output(LED_PIN, GPIO.HIGH if payload.upper() == "ON" else GPIO.LOW)
        print(f" -> LED {'ON' if payload.upper() == 'ON' else 'OFF'}")


client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()
client.loop_background()

try:
    while True:
        temp = round(random.uniform(26.0, 32.0), 1)
        client.publish(FEED_TEMP, temp)
        print(f"[PUB] Feed {FEED_TEMP} -> {temp}")
        time.sleep(10)   # free tier: max 30 data points/minute
except KeyboardInterrupt:
    client.disconnect()
    GPIO.cleanup()
    print("Adafruit IO client stopped.")
