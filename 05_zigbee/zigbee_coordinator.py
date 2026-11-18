import serial
import time

# Works on Python 2.7 and 3.5+ (no f-strings).
# XBee on GPIO pins -> '/dev/serial0' ; XBee on USB Explorer -> '/dev/ttyUSB0'
PORT = '/dev/serial0'

zigbee = serial.Serial(PORT, baudrate=9600, timeout=1)
packet_count = 0

print("Zigbee Coordinator (Transmitter) Initialized on Raspberry Pi ({})...".format(PORT))

try:
    while True:
        packet_count += 1
        simulated_temp = round(28.5 + (packet_count % 4) * 0.5, 1)

        # Transmit command and telemetry payload over Zigbee RF link
        tx_on = "CMD:ON|TEMP:{}\n".format(simulated_temp)
        zigbee.write(tx_on.encode('utf-8'))
        print("[TX Packet #{}] Sent -> {}".format(packet_count, tx_on.strip()))
        time.sleep(2)

        tx_off = "CMD:OFF|TEMP:28.0\n"
        zigbee.write(tx_off.encode('utf-8'))
        print("[TX Status] Sent -> {}".format(tx_off.strip()))
        time.sleep(2)
except KeyboardInterrupt:
    zigbee.close()
    print("Coordinator transmission stopped.")
