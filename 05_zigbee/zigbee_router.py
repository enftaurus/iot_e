import serial
import RPi.GPIO as GPIO

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

zigbee = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
print("Zigbee Router/End-Device (Receiver) Ready on Raspberry Pi...")

try:
    while True:
        if zigbee.in_waiting > 0:
            frame = zigbee.readline().decode('utf-8', errors='ignore').strip()
            if frame:
                print(f"[RX Zigbee Frame] Received: {frame}")
                if frame.startswith("CMD:ON"):
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    print(" -> Actuator State: GPIO18 HIGH (LED TURNED ON)")
                elif frame.startswith("CMD:OFF"):
                    GPIO.output(LED_PIN, GPIO.LOW)
                    print(" -> Actuator State: GPIO18 LOW (LED TURNED OFF)")
except KeyboardInterrupt:
    GPIO.cleanup()
    zigbee.close()
