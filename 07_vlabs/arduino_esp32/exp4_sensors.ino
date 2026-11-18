// Exp 4: Ultrasonic (HC-SR04), PIR, DHT22/DHT11, soil moisture, MQ135 with Arduino UNO
// Library: "DHT sensor library" by Adafruit (+ Adafruit Unified Sensor)
#include <DHT.h>

const int TRIG_PIN = 9, ECHO_PIN = 10;
const int PIR_PIN = 2;
const int DHT_PIN = 4;
const int SOIL_PIN = A0;
const int MQ135_PIN = A1;
const int LED_PIN = 13;

DHT dht(DHT_PIN, DHT22);   // change to DHT11 if that is the module

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);   // us
  return duration * 0.0343 / 2.0;                   // speed of sound 343 m/s, round trip
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT); pinMode(ECHO_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
}

void loop() {
  float dist = readDistanceCm();
  bool motion = digitalRead(PIR_PIN) == HIGH;
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  int soil = analogRead(SOIL_PIN);
  int soilPct = map(soil, 1023, 0, 0, 100);   // dry = 1023, wet = 0 (calibrate)
  int air = analogRead(MQ135_PIN);

  digitalWrite(LED_PIN, motion ? HIGH : LOW);

  Serial.print("Dist: "); Serial.print(dist); Serial.print(" cm | ");
  Serial.print("Motion: "); Serial.print(motion ? "YES" : "NO"); Serial.print(" | ");
  Serial.print("Temp: "); Serial.print(t); Serial.print(" C | ");
  Serial.print("Hum: "); Serial.print(h); Serial.print(" % | ");
  Serial.print("Soil: "); Serial.print(soilPct); Serial.print(" % | ");
  Serial.print("Air(MQ135 raw): "); Serial.println(air);
  delay(2000);
}
