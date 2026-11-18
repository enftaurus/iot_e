# Bluetooth: control an LED from a phone

The Pi runs an RFCOMM (Serial Port Profile) server. A phone sends `ON` or `OFF` and the LED on GPIO18 follows.

## One-time setup on the Pi

```bash
sudo apt install -y bluetooth bluez
hciconfig                      # note the Pi's BD Address -> put it in PI_BT_MAC

# Enable SPP so phones can see the serial service
sudo nano /lib/systemd/system/bluetooth.service
#   change:  ExecStart=/usr/libexec/bluetooth/bluetoothd
#   to:      ExecStart=/usr/libexec/bluetooth/bluetoothd -C
sudo systemctl daemon-reload && sudo systemctl restart bluetooth
sudo sdptool add SP

# Make the Pi discoverable and pair with the phone
bluetoothctl
  power on
  discoverable on
  pairable on
  agent on
  default-agent
  # pair from the phone now, type "yes" to confirm
```

## Run

```bash
sudo python3 bt_led_server.py
```

On the phone, open **Serial Bluetooth Terminal**, go to Devices, tap the Pi, and send `ON` / `OFF`.

## Expected output

```
Bluetooth RFCOMM Server waiting on channel 1...
[BT] Connected to device: 7C:XX:XX:XX:XX:XX
[RX Bluetooth] Received: ON
 -> GPIO18 HIGH (LED TURNED ON)
[RX Bluetooth] Received: OFF
 -> GPIO18 LOW (LED TURNED OFF)
```

## Files

| File | Purpose |
|---|---|
| `bt_led_server.py` | Main program: Pi receives commands and drives the LED |
| `bt_client.py` | Pi-to-Pi version, if the examiner wants two boards |
| `bt_scan.py` | Lists nearby Bluetooth devices |

## Viva points

- Classic Bluetooth uses the 2.4 GHz ISM band with FHSS (79 channels, 1 MHz apart, 1600 hops/s) and has a range of about 10 m.
- RFCOMM emulates a serial port over L2CAP. SPP is the profile that uses it.
- BLE (Bluetooth Low Energy) is a different radio mode built around GATT services and characteristics. It's low power and suited to sensors.
- A piconet has 1 master and up to 7 active slaves.
