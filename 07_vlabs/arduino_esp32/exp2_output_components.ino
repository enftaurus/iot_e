// Exp 2: Output components (RGB LED, 7-segment, OLED, LCD 16x2, buzzer) with Arduino UNO
// Libraries (Library Manager): Adafruit SSD1306, Adafruit GFX, LiquidCrystal I2C
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <LiquidCrystal_I2C.h>

// RGB LED (common cathode) on PWM pins
const int R_PIN = 9, G_PIN = 10, B_PIN = 6;   // not 3/11: tone() uses Timer2 and kills PWM there
const int BUZZER_PIN = 8;
// 7-segment (common cathode) segments a..g -> D2, D3, D4, D5, D7, D12, D13
const int SEG[7] = {2, 3, 4, 5, 7, 12, 13};
const byte DIGITS[10] = {        // gfedcba
  0b0111111, 0b0000110, 0b1011011, 0b1001111, 0b1100110,
  0b1101101, 0b1111101, 0b0000111, 0b1111111, 0b1101111
};

Adafruit_SSD1306 oled(128, 64, &Wire, -1);   // OLED I2C 0x3C, SDA=A4, SCL=A5
LiquidCrystal_I2C lcd(0x27, 16, 2);          // LCD I2C backpack 0x27

void setRGB(int r, int g, int b) {
  analogWrite(R_PIN, r); analogWrite(G_PIN, g); analogWrite(B_PIN, b);
}

void showDigit(int d) {
  for (int i = 0; i < 7; i++) digitalWrite(SEG[i], bitRead(DIGITS[d], i));
}

void setup() {
  Serial.begin(9600);
  pinMode(R_PIN, OUTPUT); pinMode(G_PIN, OUTPUT); pinMode(B_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  for (int i = 0; i < 7; i++) pinMode(SEG[i], OUTPUT);

  oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);

  lcd.init();
  lcd.backlight();
}

void loop() {
  for (int n = 0; n < 10; n++) {
    // RGB cycles R -> G -> B
    if (n % 3 == 0) setRGB(255, 0, 0);
    else if (n % 3 == 1) setRGB(0, 255, 0);
    else setRGB(0, 0, 255);

    showDigit(n);

    oled.clearDisplay();
    oled.setCursor(0, 0);  oled.println("IoT VLab Output");
    oled.setCursor(0, 20); oled.print("Count: "); oled.println(n);
    oled.display();

    lcd.setCursor(0, 0); lcd.print("Hello IoT Lab  ");
    lcd.setCursor(0, 1); lcd.print("Count: "); lcd.print(n); lcd.print("   ");

    tone(BUZZER_PIN, 1000, 150);   // 1 kHz beep for 150 ms
    Serial.print("Count = "); Serial.println(n);
    delay(1000);
  }
}
