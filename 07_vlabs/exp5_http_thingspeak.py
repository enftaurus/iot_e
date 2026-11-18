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
        print(f"[HTTP {r.status_code}] Temp: {temp} C | Humidity: {hum} % -> Entry ID: {r.text}")

        # Read back the latest entry (HTTP GET /feeds/last.json)
        last = requests.get(f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json",
                            params={"api_key": READ_KEY}, timeout=10).json()
        print(f"   Last on cloud: field1={last.get('field1')} field2={last.get('field2')} "
              f"at {last.get('created_at')}")

        time.sleep(20)   # free tier: one update per 15 s
except KeyboardInterrupt:
    dht.exit()
    print("Stopped.")
