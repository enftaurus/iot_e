import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Subscribes to the LED + temp topics; drives GPIO18 LED from MQTT messages.

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_TEMP = "vce/iot/temp"
TOPIC_LED = "vce/iot/led"

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker {} (rc={})".format(BROKER, rc))
    client.subscribe([(TOPIC_TEMP, 1), (TOPIC_LED, 1)])
    print("Subscribed to {} and {}".format(TOPIC_TEMP, TOPIC_LED))


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("[SUB] {} -> {}".format(msg.topic, payload))
    if msg.topic == TOPIC_LED:
        if payload == "ON":
            GPIO.output(LED_PIN, GPIO.HIGH)
            print(" -> GPIO18 HIGH (LED TURNED ON)")
        elif payload == "OFF":
            GPIO.output(LED_PIN, GPIO.LOW)
            print(" -> GPIO18 LOW (LED TURNED OFF)")


client = mqtt.Client("vce_pi_subscriber")   # paho 1.x style; on paho 2.x use mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "vce_pi_subscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    GPIO.cleanup()
    print("Subscriber stopped.")
