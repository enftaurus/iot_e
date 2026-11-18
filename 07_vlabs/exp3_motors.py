import time
import RPi.GPIO as GPIO

# Exp 3: DC motor (L298N), servo (SG90) and stepper (28BYJ-48 + ULN2003)
# Power motors from an external 5 V supply; share GND with the Pi.

IN1, IN2, ENA = 23, 24, 25          # L298N
SERVO_PIN = 18                      # SG90 signal
STEP_PINS = [17, 27, 22, 4]         # ULN2003 IN1..IN4

# Half-step sequence for 28BYJ-48 (4096 half-steps = 1 revolution)
HALF_STEP = [
    [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
    [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1],
]
STEPS_PER_REV = 4096

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([IN1, IN2, ENA, SERVO_PIN] + STEP_PINS, GPIO.OUT, initial=GPIO.LOW)

dc_pwm = GPIO.PWM(ENA, 1000)        # 1 kHz speed control
dc_pwm.start(0)
servo = GPIO.PWM(SERVO_PIN, 50)     # servo needs 50 Hz (20 ms period)
servo.start(0)


def set_angle(angle):
    duty = 2.5 + angle / 18          # 0 deg = 2.5 % (0.5 ms), 180 deg = 12.5 % (2.5 ms)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)         # stop jitter


def stepper(steps, direction=1, delay=0.001):
    seq = HALF_STEP if direction == 1 else HALF_STEP[::-1]
    for i in range(steps):
        for pin, val in zip(STEP_PINS, seq[i % 8]):
            GPIO.output(pin, val)
        time.sleep(delay)
    GPIO.output(STEP_PINS, GPIO.LOW)


print("Motor Control Demo Started on Raspberry Pi...")

try:
    while True:
        print("DC Motor: FORWARD (75% speed)")
        GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
        dc_pwm.ChangeDutyCycle(75)
        time.sleep(2)
        print("DC Motor: REVERSE")
        GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
        time.sleep(2)
        print("DC Motor: STOP")
        dc_pwm.ChangeDutyCycle(0)

        for angle in (0, 90, 180, 90, 0):
            set_angle(angle)
            print(f"Servo -> {angle} deg")

        print("Stepper: 1 revolution CW")
        stepper(STEPS_PER_REV, 1)
        print("Stepper: 1 revolution CCW")
        stepper(STEPS_PER_REV, -1)
        time.sleep(1)
except KeyboardInterrupt:
    dc_pwm.stop()
    servo.stop()
    GPIO.cleanup()
    print("Stopped.")
