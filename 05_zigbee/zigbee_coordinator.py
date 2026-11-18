import serial
import time

# XBee Coordinator plugged into Raspberry Pi via USB Explorer.
# Find the port with: ls /dev/ttyUSB*   (Windows PC: 'COM3')
PORT = '/dev/ttyUSB0'

# Initialize serial (COM) port connected to XBee Coordinator
zigbee = serial.Serial(PORT, baudrate=9600, timeout=1)
packet_count = 0

print(f"Zigbee Coordinator (Transmitter) Initialized on Raspberry Pi ({PORT})...")

try:
    while True:
        packet_count += 1
        simulated_temp = round(28.5 + (packet_count % 4) * 0.5, 1)

        # Transmit command and telemetry payload over Zigbee RF link
        tx_on = f"CMD:ON|TEMP:{simulated_temp}\n"
        zigbee.write(tx_on.encode('utf-8'))
        print(f"[TX Packet #{packet_count}] Sent -> {tx_on.strip()}")
        time.sleep(2)

        tx_off = "CMD:OFF|TEMP:28.0\n"
        zigbee.write(tx_off.encode('utf-8'))
        print(f"[TX Status] Sent -> {tx_off.strip()}")
        time.sleep(2)
except KeyboardInterrupt:
    zigbee.close()
    print("Coordinator transmission stopped.")
