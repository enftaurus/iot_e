import time
import paho.mqtt.client as mqtt

# Publishes simulated temperature + LED commands to a public broker.
# For a local broker: sudo apt install mosquitto mosquitto-clients, then BROKER = "localhost"

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_TEMP = "vce/iot/temp"
TOPIC_LED = "vce/iot/led"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker {} (rc={})".format(BROKER, rc))


client = mqtt.Client("vce_pi_publisher")   # paho 1.x style; on paho 2.x use mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "vce_pi_publisher")
client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

count = 0
try:
    while True:
        count += 1
        temp = round(28.0 + (count % 5) * 0.4, 1)
        client.publish(TOPIC_TEMP, temp, qos=1)
        print("[PUB #{}] {} -> {}".format(count, TOPIC_TEMP, temp))

        cmd = "ON" if count % 2 else "OFF"
        client.publish(TOPIC_LED, cmd, qos=1)
        print("[PUB #{}] {} -> {}".format(count, TOPIC_LED, cmd))
        time.sleep(3)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Publisher stopped.")
