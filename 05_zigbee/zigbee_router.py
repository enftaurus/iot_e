import serial
import RPi.GPIO as GPIO

# Works on Python 2.7 and 3.5+ (no f-strings).
# XBee on GPIO pins -> '/dev/serial0' ; XBee on USB Explorer -> '/dev/ttyUSB0'
PORT = '/dev/serial0'

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

zigbee = serial.Serial(PORT, baudrate=9600, timeout=1)
print("Zigbee Router/End-Device (Receiver) Ready on Raspberry Pi ({})...".format(PORT))

try:
    while True:
        if zigbee.in_waiting > 0:
            frame = zigbee.readline().decode('utf-8', 'ignore').strip()
            if frame:
                print("[RX Zigbee Frame] Received: {}".format(frame))
                if frame.startswith("CMD:ON"):
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    print(" -> Actuator State: GPIO18 HIGH (LED TURNED ON)")
                elif frame.startswith("CMD:OFF"):
                    GPIO.output(LED_PIN, GPIO.LOW)
                    print(" -> Actuator State: GPIO18 LOW (LED TURNED OFF)")
except KeyboardInterrupt:
    GPIO.cleanup()
    zigbee.close()
