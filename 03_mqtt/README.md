# MQTT

There are two ways to run this. Do whichever the examiner asks for.

## A. Public broker (paho-mqtt)

```bash
pip3 install paho-mqtt            # v2.x (the code uses CallbackAPIVersion.VERSION2)
# Terminal 1
python3 mqtt_subscriber.py
# Terminal 2 (same Pi or another Pi / laptop)
python3 mqtt_publisher.py
```

Quick test without Python, using `sudo apt install mosquitto-clients`:

```bash
mosquitto_sub -h test.mosquitto.org -t "vce/iot/#" -v
mosquitto_pub -h test.mosquitto.org -t "vce/iot/led" -m "ON"
```

If you need a local broker instead: `sudo apt install mosquitto`, then set `BROKER = "localhost"` in the code.

> **paho v1 error?** If you see `AttributeError: CallbackAPIVersion`, the Pi has paho 1.x. Either upgrade it (`pip3 install -U paho-mqtt`), or change the code to `mqtt.Client("id")` and use `on_connect(client, userdata, flags, rc)` with 4 arguments.

## B. Adafruit IO (cloud dashboard)

```bash
pip3 install adafruit-io
python3 adafruit_io_mqtt.py
```

Set up the feeds and dashboard as described in the comments at the top of the file. Flipping the toggle on the dashboard turns the LED on or off, and the temperature gauge updates every 10 s.

## Expected output (A)

```
Connected to MQTT Broker test.mosquitto.org (rc=Success)
Subscribed to vce/iot/temp and vce/iot/led
[SUB] vce/iot/temp -> 28.4
[SUB] vce/iot/led -> ON
 -> GPIO18 HIGH (LED TURNED ON)
```

## Viva points

- MQTT is a publish/subscribe protocol that runs over TCP. Port 1883 is plain and 8883 uses TLS. It's an OASIS / ISO standard.
- The **broker** (Mosquitto, Adafruit IO, HiveMQ) routes messages. Publishers and subscribers never talk to each other directly.
- **QoS 0** means at most once (fire and forget). **QoS 1** means at least once (PUBACK). **QoS 2** means exactly once (a 4-step handshake).
- Wildcards: `+` matches one level (`vce/+/temp`) and `#` matches all remaining levels (`vce/#`).
- With a **retained message**, the broker keeps the last value and sends it to new subscribers.
- **LWT (Last Will)** is a message the broker publishes if a client drops unexpectedly.
- **Keep-alive** works through PINGREQ/PINGRESP packets.
