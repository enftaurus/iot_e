import RPi.GPIO as GPIO
import time

# Optional variant: mix any colour using PWM (0-100 % duty cycle per channel)
RED_PIN, GREEN_PIN, BLUE_PIN = 17, 27, 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([RED_PIN, GREEN_PIN, BLUE_PIN], GPIO.OUT)

red = GPIO.PWM(RED_PIN, 100)     # 100 Hz
green = GPIO.PWM(GREEN_PIN, 100)
blue = GPIO.PWM(BLUE_PIN, 100)
for ch in (red, green, blue):
    ch.start(0)

print("RGB PWM fade started...")

try:
    while True:
        for duty in range(0, 101, 5):          # red fades up, blue fades down
            red.ChangeDutyCycle(duty)
            blue.ChangeDutyCycle(100 - duty)
            time.sleep(0.05)
        for duty in range(0, 101, 5):          # green fades up, red fades down
            green.ChangeDutyCycle(duty)
            red.ChangeDutyCycle(100 - duty)
            time.sleep(0.05)
        for duty in range(0, 101, 5):          # blue fades up, green fades down
            blue.ChangeDutyCycle(duty)
            green.ChangeDutyCycle(100 - duty)
            time.sleep(0.05)
        print("Fade cycle complete")
except KeyboardInterrupt:
    for ch in (red, green, blue):
        ch.stop()
    GPIO.cleanup()
    print("PWM fade stopped.")
