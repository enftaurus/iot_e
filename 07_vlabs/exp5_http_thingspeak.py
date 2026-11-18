import time
import board
import requests
import adafruit_dht

# Exp 5: Send live sensor data to ThingSpeak over HTTP (REST API)
# Also reads the last values back (HTTP GET on the channel feed).

WRITE_KEY = "XXXXXXXXXXXXXXXX"
READ_KEY = "YYYYYYYYYYYYYYYY"
CHANNEL_ID = "0000000"

dht = adafruit_dht.DHT11(board.D4)
print("HTTP -> ThingSpeak uploader started on Raspberry Pi...")

try:
    while True:
        try:
            temp, hum = dht.temperature, dht.humidity
        except RuntimeError:
            time.sleep(2)
            continue

        # Upload (HTTP GET /update)
        r = requests.get("https://api.thingspeak.com/update",
                         params={"api_key": WRITE_KEY, "field1": temp, "field2": hum},
                         timeout=10)
        print("[HTTP {}] Temp: {} C | Humidity: {} % -> Entry ID: {}".format(r.status_code, temp, hum, r.text))

        # Read back the latest entry (HTTP GET /feeds/last.json)
        last = requests.get("https://api.thingspeak.com/channels/{}/feeds/last.json".format(CHANNEL_ID),
                            params={"api_key": READ_KEY}, timeout=10).json()
        print("   Last on cloud: field1={} field2={} ".format(last.get('field1'), last.get('field2')) +
              "at {}".format(last.get('created_at')))

        time.sleep(20)   # free tier: one update per 15 s
except KeyboardInterrupt:
    dht.exit()
    print("Stopped.")
