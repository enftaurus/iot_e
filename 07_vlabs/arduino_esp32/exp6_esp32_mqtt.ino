// Exp 6: Send live sensor data over MQTT using ESP32 (PubSubClient library)
// Public broker test.mosquitto.org - watch with:  mosquitto_sub -h test.mosquitto.org -t "vce/esp32/#" -v
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";
const char* BROKER = "test.mosquitto.org";
const int LED_PIN = 2;

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(15, DHT22);

void callback(char* topic, byte* payload, unsigned int len) {
  String msg;
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];
  Serial.printf("[SUB] %s -> %s\n", topic, msg.c_str());
  if (String(topic) == "vce/esp32/led") digitalWrite(LED_PIN, msg == "ON" ? HIGH : LOW);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    String id = "esp32-" + String(random(0xffff), HEX);
    if (client.connect(id.c_str())) {
      Serial.println("connected");
      client.subscribe("vce/esp32/led");
    } else {
      Serial.printf("failed rc=%d, retry in 2s\n", client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("WiFi connected");
  client.setServer(BROKER, 1883);
  client.setCallback(callback);
}

unsigned long lastPub = 0;
void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  if (millis() - lastPub > 5000) {
    lastPub = millis();
    String t = String(dht.readTemperature(), 1);
    String h = String(dht.readHumidity(), 1);
    client.publish("vce/esp32/temp", t.c_str());
    client.publish("vce/esp32/hum", h.c_str());
    Serial.println("[PUB] temp=" + t + " hum=" + h);
  }
}
