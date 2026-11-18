// Exp 3: DC motor (via L293D/L298N), servo and stepper (via A4988 / ULN2003) with Arduino UNO
#include <Servo.h>
#include <Stepper.h>

// DC motor through L298N: IN1, IN2 direction, ENA speed (PWM)
const int IN1 = 7, IN2 = 8, ENA = 5;
// Servo signal
const int SERVO_PIN = 6;
// Stepper (28BYJ-48 + ULN2003): IN1..IN4 -> 9, 10, 11, 12 ; 2048 steps/rev
const int STEPS_PER_REV = 2048;
Stepper stepper(STEPS_PER_REV, 9, 11, 10, 12);
Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT); pinMode(ENA, OUTPUT);
  servo.attach(SERVO_PIN);
  stepper.setSpeed(10);   // RPM
}

void loop() {
  // DC motor forward then reverse
  Serial.println("DC Motor: FORWARD");
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); analogWrite(ENA, 200);
  delay(2000);
  Serial.println("DC Motor: REVERSE");
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  delay(2000);
  Serial.println("DC Motor: STOP");
  analogWrite(ENA, 0);

  // Servo sweep 0 -> 180 -> 0
  for (int a = 0; a <= 180; a += 10) { servo.write(a); delay(50); }
  for (int a = 180; a >= 0; a -= 10) { servo.write(a); delay(50); }
  Serial.println("Servo: swept 0-180-0");

  // Stepper one revolution each way
  Serial.println("Stepper: CW 1 rev");
  stepper.step(STEPS_PER_REV);
  Serial.println("Stepper: CCW 1 rev");
  stepper.step(-STEPS_PER_REV);
  delay(1000);
}
