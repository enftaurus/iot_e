import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Exp 6: Send live sensor data over MQTT + receive LED commands
# Watch from a laptop:  mosquitto_sub -h test.mosquitto.org -t "vce/pi/#" -v
# Control LED:          mosquitto_pub -h test.mosquitto.org -t "vce/pi/led" -m ON

BROKER = "test.mosquitto.org"
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
dht = adafruit_dht.DHT11(board.D4)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT Broker {BROKER} (rc={reason_code})")
    client.subscribe("vce/pi/led")


def on_message(client, userdata, msg):
    cmd = msg.payload.decode().upper()
    print(f"[SUB] {msg.topic} -> {cmd}")
    GPIO.output(LED_PIN, cmd == "ON")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="vce_pi_sensor")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        try:
            temp, hum = dht.temperature, dht.humidity
            client.publish("vce/pi/temp", temp)
            client.publish("vce/pi/hum", hum)
            print(f"[PUB] temp={temp} C hum={hum} %")
        except RuntimeError:
            pass
        time.sleep(5)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    dht.exit()
    GPIO.cleanup()
    print("Stopped.")
