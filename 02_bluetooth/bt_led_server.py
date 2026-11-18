import socket
import RPi.GPIO as GPIO

# Raspberry Pi acts as a Bluetooth (Classic, RFCOMM / SPP) server.
# A phone running "Serial Bluetooth Terminal" (Android) connects and sends ON / OFF.
# Uses Python's built-in Bluetooth sockets - no pybluez needed.

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

PI_BT_MAC = "B8:27:EB:XX:XX:XX"   # <- replace: run `hciconfig` or `bluetoothctl show`
CHANNEL = 1                       # RFCOMM channel (SPP default)

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((PI_BT_MAC, CHANNEL))
server.listen(1)
print(f"Bluetooth RFCOMM Server waiting on channel {CHANNEL}...")

client = None
try:
    client, addr = server.accept()
    print(f"[BT] Connected to device: {addr[0]}")
    client.send(b"Connected to Raspberry Pi. Send ON / OFF\n")

    while True:
        data = client.recv(1024)
        if not data:
            break
        cmd = data.decode("utf-8", errors="ignore").strip().upper()
        print(f"[RX Bluetooth] Received: {cmd}")

        if cmd == "ON":
            GPIO.output(LED_PIN, GPIO.HIGH)
            client.send(b"LED ON\n")
            print(" -> GPIO18 HIGH (LED TURNED ON)")
        elif cmd == "OFF":
            GPIO.output(LED_PIN, GPIO.LOW)
            client.send(b"LED OFF\n")
            print(" -> GPIO18 LOW (LED TURNED OFF)")
        else:
            client.send(b"Unknown command\n")
except KeyboardInterrupt:
    pass
finally:
    if client:
        client.close()
    server.close()
    GPIO.cleanup()
    print("Bluetooth server stopped.")
