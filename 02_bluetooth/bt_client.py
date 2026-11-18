import socket
import time

# Pi-to-Pi variant: run this on a second Raspberry Pi (or a Linux laptop)
# to send commands to bt_led_server.py instead of using a phone.

SERVER_MAC = "B8:27:EB:XX:XX:XX"   # <- MAC of the Pi running bt_led_server.py
CHANNEL = 1

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((SERVER_MAC, CHANNEL))
print("Connected to Bluetooth server {}".format(SERVER_MAC))
print(sock.recv(1024).decode().strip())

try:
    while True:
        for cmd in ("ON", "OFF"):
            sock.send(cmd.encode())
            print("[TX Bluetooth] Sent -> {}".format(cmd))
            print("[Reply] {}".format(sock.recv(1024).decode().strip()))
            time.sleep(2)
except KeyboardInterrupt:
    sock.close()
    print("Bluetooth client stopped.")
