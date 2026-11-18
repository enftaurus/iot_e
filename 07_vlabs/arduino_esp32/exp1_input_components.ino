// Exp 1: Input components (pushbutton, potentiometer, slider switch, photoresistor/LDR) with Arduino UNO
const int BUTTON_PIN = 2;   // pushbutton -> D2 (INPUT_PULLUP, other leg to GND)
const int SLIDE_PIN  = 3;   // slider switch middle pin -> D3
const int POT_PIN    = A0;  // potentiometer wiper -> A0
const int LDR_PIN    = A1;  // LDR + 10k divider -> A1
const int LED_PIN    = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(SLIDE_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  bool pressed = digitalRead(BUTTON_PIN) == LOW;
  bool slideOn = digitalRead(SLIDE_PIN) == LOW;
  int pot = analogRead(POT_PIN);            // 0-1023
  int light = analogRead(LDR_PIN);          // 0-1023

  digitalWrite(LED_PIN, pressed ? HIGH : LOW);

  Serial.print("Button: "); Serial.print(pressed ? "PRESSED" : "RELEASED");
  Serial.print(" | Slide: "); Serial.print(slideOn ? "ON" : "OFF");
  Serial.print(" | Pot: "); Serial.print(pot);
  Serial.print(" ("); Serial.print(map(pot, 0, 1023, 0, 100)); Serial.print("%)");
  Serial.print(" | LDR: "); Serial.println(light);
  delay(500);
}
