// Exp 5: Send live sensor data to ThingSpeak over HTTP using ESP32
// In Wokwi / vlab simulator use SSID "Wokwi-GUEST" with empty password.
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";
const String WRITE_KEY = "XXXXXXXXXXXXXXXX";   // ThingSpeak Write API Key

DHT dht(15, DHT22);   // DHT data -> GPIO15

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi connected, IP: " + WiFi.localIP().toString());
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  Serial.printf("Temp: %.1f C | Humidity: %.1f %%\n", t, h);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://api.thingspeak.com/update?api_key=" + WRITE_KEY +
                 "&field1=" + String(t) + "&field2=" + String(h);
    http.begin(url);
    int code = http.GET();
    Serial.printf("HTTP %d, entry id: %s\n", code, http.getString().c_str());
    http.end();
  }
  delay(20000);   // ThingSpeak free: >= 15 s between updates
}
