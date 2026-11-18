# Zigbee: Theory and How to Set It Up

**Platform:** 2 × Raspberry Pi, 2 × Digi XBee S2C (Zigbee) modules, the XCTU configuration tool, and Python `pyserial`.
**Programs:** `zigbee_coordinator.py` (transmitter) and `zigbee_router.py` (receiver + LED).

---

## 1. Aim

To show wireless communication between two IoT nodes using the Zigbee protocol. The **Coordinator** sends a command and telemetry (`CMD:ON|TEMP:29.0`). The **Router/End Device** receives it and switches an LED on GPIO18.

## 2. What is Zigbee?

Zigbee is a **low-power, low-data-rate, short-range wireless mesh networking** standard maintained by the **Connectivity Standards Alliance (CSA)**, formerly the Zigbee Alliance. It is built on top of **IEEE 802.15.4**, which defines the physical (PHY) and MAC layers.

It's used in home and building automation, smart lighting (Philips Hue), smart meters, industrial sensor networks, and healthcare monitoring.

### Key specifications

| Parameter | Value |
|---|---|
| Base standard | IEEE 802.15.4 (PHY + MAC) |
| Frequency | **2.4 GHz** (worldwide, 16 channels: 11–26), 915 MHz (US), 868 MHz (EU) |
| Data rate | **250 kbps** at 2.4 GHz (40 kbps at 915 MHz, 20 kbps at 868 MHz) |
| Range | 10–100 m indoors per hop (XBee S2C: ~60 m indoor, ~1200 m line of sight). Mesh extends the range |
| Modulation | O-QPSK with DSSS at 2.4 GHz |
| Max nodes | Up to **65,000** per network (16-bit short address) |
| Addressing | 64-bit IEEE (MAC) address + 16-bit network address |
| Security | **AES-128** encryption, network and link keys |
| Power | Very low. Battery nodes can last for years thanks to sleep modes |
| Topologies | Star, Tree, **Mesh** |
| Channel access | CSMA-CA |

## 3. Zigbee protocol stack

```
+------------------------------------------+
|  Application Layer (APL)                 |
|   - Application Framework (endpoints)    |
|   - ZDO (Zigbee Device Object)           |  <- Zigbee Alliance / CSA
|   - APS (Application Support Sublayer)   |
+------------------------------------------+
|  Network Layer (NWK)                     |  <- routing, addressing, joining, security
+------------------------------------------+
|  MAC Layer                               |  <- IEEE 802.15.4: CSMA-CA, ACKs, beacons
+------------------------------------------+
|  Physical Layer (PHY)                    |  <- IEEE 802.15.4: radio, channel, modulation
+------------------------------------------+
```

- **PHY** handles the radio: transmitting and receiving, channel selection, energy detection, and the link quality indicator (LQI).
- **MAC** handles framing, CSMA-CA channel access, acknowledgements and beacons.
- **NWK** handles joining and leaving the network, address assignment, route discovery (AODV-based mesh routing) and network security.
- **APS** handles binding (linking devices), group addressing, fragmentation and end-to-end delivery.
- **ZDO** manages the device's role (coordinator/router/end device), discovery and security.
- **Application Framework** holds up to 240 endpoints that use **ZCL** (Zigbee Cluster Library) clusters such as On/Off, Level, and Temperature Measurement.

## 4. Device types

| Device | Role | Routes? | Can sleep? | Count |
|---|---|---|---|---|
| **Coordinator (ZC)** | Starts the network, picks the channel and PAN ID, acts as Trust Center (security keys) | Yes | No (mains powered) | **Exactly 1** per network |
| **Router (ZR)** | Relays packets, lets new nodes join, extends range | Yes | No | Many |
| **End Device (ZED)** | Sensor or actuator that talks only to its parent | No | **Yes** (battery) | Many |

By IEEE 802.15.4 terms, a **FFD** (Full Function Device) can act as coordinator or router, while a **RFD** (Reduced Function Device) can only be an end device.

## 5. Topologies

```
   STAR                TREE                     MESH
                        ZC                    ZC ---- ZR
    ZED                /  \                    | \   / |
     |               ZR    ZR                  |  ZR   |
ZED-ZC-ZED          / \     \                  | /   \ |
     |            ZED ZED   ZED               ZR ---- ZR --- ZED
    ZED
```

- **Star**: every node talks only to the coordinator. It's simple, but the coordinator is a single point of failure.
- **Tree**: routers forward packets up and down a hierarchy.
- **Mesh**: there are multiple paths, so the network is self-healing. If a router fails, traffic is rerouted. This is Zigbee's main strength.

In our lab, 2 nodes form a simple **point-to-point (star)** link: Coordinator → Router.

## 6. Zigbee vs other IoT protocols

| | Zigbee | Bluetooth (Classic/BLE) | Wi-Fi | LoRa |
|---|---|---|---|---|
| Standard | IEEE 802.15.4 | IEEE 802.15.1 / BT SIG | IEEE 802.11 | LoRa Alliance |
| Data rate | 250 kbps | 1–3 Mbps / 1–2 Mbps | 11 Mbps–Gbps | 0.3–50 kbps |
| Range | 10–100 m (mesh extends it) | ~10 m (BLE up to ~100 m) | ~50–100 m | 2–15 km |
| Power | Very low | Low (BLE very low) | High | Very low |
| Topology | Mesh/Star/Tree | Piconet / star | Star | Star-of-stars |
| Max nodes | 65,000 | 7 active (classic) | ~250 per AP | Thousands |
| Use | Home/industrial sensor mesh | Wearables, audio, phones | High-bandwidth, internet | Long-range agriculture/city |

---

## 7. Platform: hardware needed

- 2 × Raspberry Pi (3B+/4) with Raspberry Pi OS
- 2 × **Digi XBee S2C** (Zigbee 3.0) modules (Series 1 XBee modules are plain 802.15.4, *not* Zigbee)
- 1 × **XBee USB Explorer / adapter board**, used to configure the modules from a PC
- 2 × XBee breakout/adapter boards to connect them to the Pi UART (or plug the Explorer into the Pi over USB)
- 1 × LED + 220 Ω resistor on the receiver Pi
- Jumper wires, and a PC with **XCTU** installed (free from Digi)

## 8. Step 1: Configure the XBee modules in XCTU

Put each XBee on the USB Explorer, plug it into the PC, open XCTU, click **Add device** (or **Discover**), choose the COM port and 9600 baud, and click Finish.

If needed, use **Update firmware** to pick the product family XB24C and the function set **Zigbee TH Reg**.

| Parameter | Coordinator XBee | Router XBee | Meaning |
|---|---|---|---|
| **ID** (PAN ID) | `1234` | `1234` | Must match, so both join the same network |
| **CE** (Coordinator Enable) | `1` (Enabled) | `0` (Disabled) | Makes this one the coordinator |
| **JV** (Channel Verification) | – | `1` | Router checks that the coordinator exists |
| **DH** (Destination High) | `0` | `0` | DH+DL = destination address |
| **DL** (Destination Low) | `FFFF` (broadcast) or the router's SL | `0` (= coordinator) | `0/0` always means "the coordinator" |
| **BD** (Baud rate) | `3` = 9600 | `3` = 9600 | Must match `baudrate=9600` in Python |
| **AP** (API mode) | `0` = Transparent | `0` = Transparent | Transparent mode passes serial bytes straight through. Our code uses this |
| **NI** (Node Identifier) | `COORD` | `ROUTER` | Optional label |

Click **Write** (the pencil icon) for each module.

Note down each module's **SH/SL**. This is the 64-bit address printed on the back of the module.

**Verify in XCTU:** open the Console on both modules (two Explorers or two PCs), type on one, and the text should appear on the other. You can also use the **Network** view (the globe icon) to see the topology.

> Transparent (AT) mode means: whatever goes into the coordinator's DIN pin comes out of the router's DOUT pin. That's why the Python code only needs `serial.write()` and `serial.readline()`.

## 9. Step 2: Wire the XBee to the Raspberry Pi

| XBee pin | Raspberry Pi |
|---|---|
| Pin 1 – VCC (3.3 V) | Pin 1 – 3.3 V |
| Pin 10 – GND | Pin 6 – GND |
| Pin 2 – DOUT (TX) | Pin 10 – GPIO15 (RXD) |
| Pin 3 – DIN (RX) | Pin 8 – GPIO14 (TXD) |

TX goes to RX and RX goes to TX. The XBee is a **3.3 V** device, so never connect it to 5 V.
If you use a USB Explorer on the Pi instead, change `/dev/serial0` to `/dev/ttyUSB0` in the code.

Receiver LED: GPIO18 (pin 12) → 220 Ω → LED anode (long leg). The LED cathode goes to GND.

## 10. Step 3: Enable the Pi UART (both Pis)

```bash
sudo raspi-config
#  Interface Options -> Serial Port
#   "Login shell over serial?"  -> No
#   "Serial port hardware enabled?" -> Yes
sudo reboot

ls -l /dev/serial0          # should point to ttyS0 or ttyAMA0
pip3 install pyserial       # usually preinstalled
```

On Pi 3/4, you can add `dtoverlay=disable-bt` to `/boot/firmware/config.txt` (`/boot/config.txt` on older OS). This frees up the stable PL011 UART, but it **disables Bluetooth**, so undo it before running the Bluetooth program.

## 11. Step 4: Run

```bash
# Pi B (receiver) first
python3 zigbee_router.py
# Pi A (transmitter)
python3 zigbee_coordinator.py
```

### Expected output

Coordinator:
```
Zigbee Coordinator (Transmitter) Initialized on Raspberry Pi...
[TX Packet #1] Sent -> CMD:ON|TEMP:29.0
[TX Status] Sent -> CMD:OFF|TEMP:28.0
```
Router:
```
Zigbee Router/End-Device (Receiver) Ready on Raspberry Pi...
[RX Zigbee Frame] Received: CMD:ON|TEMP:29.0
 -> Actuator State: GPIO18 HIGH (LED TURNED ON)
[RX Zigbee Frame] Received: CMD:OFF|TEMP:28.0
 -> Actuator State: GPIO18 LOW (LED TURNED OFF)
```
The LED on the receiver blinks ON and OFF every 2 s.

## 12. How the code works

- `serial.Serial('/dev/serial0', 9600)` opens the Pi's UART, which is wired to the XBee.
- The **Coordinator** builds a text frame `CMD:ON|TEMP:x` and calls `.encode()` to turn it into bytes. `zigbee.write()` sends it to the XBee, and the XBee transmits it over 2.4 GHz to DH/DL.
- The **Router's** XBee receives the RF packet and outputs it on its UART. `in_waiting > 0` checks whether bytes have arrived, then `readline()` reads up to `\n`.
- `startswith("CMD:ON")` parses the command and sets `GPIO.output(18, HIGH/LOW)`.
- `\n` is the frame delimiter. `try/except KeyboardInterrupt` closes the port and runs GPIO cleanup.

## 13. Troubleshooting

| Problem | Fix |
|---|---|
| Nothing received | Check that the PAN IDs match, that only one module has CE=1, and that the router's DL=0 |
| Garbage characters | The baud rate in XCTU (BD) doesn't match the code |
| `Permission denied /dev/serial0` | `sudo usermod -aG dialout pi` and log in again, or run with `sudo` |
| `/dev/serial0` missing | The serial port isn't enabled in raspi-config |
| Router never joins | Its Associate LED isn't blinking. Power the coordinator first and check JV=1 |

## 14. Alternative platforms (if asked "how else can Zigbee be done?")

- **Arduino/ESP32 + XBee**: same XCTU setup. Use `SoftwareSerial` or `Serial2` and `Serial.print("CMD:ON")`.
- **XBee API mode (AP=1/2) + `digi-xbee` Python library**: structured frames with source address, RSSI and checksum, plus remote AT commands. Code looks like `XBeeDevice("/dev/ttyUSB0", 9600).send_data_broadcast("hello")`.
- **Zigbee2MQTT / Home Assistant**: a USB Zigbee coordinator dongle (e.g. Sonoff ZBDongle, CC2652) on the Pi bridges commercial Zigbee bulbs and sensors to MQTT topics. This ties Zigbee and MQTT together.
- **Simulation**: if no hardware is available, run the same code with a USB-to-serial loopback, or simulate 802.15.4 in Cooja/Contiki or NS-3.

## 15. Viva questions

1. **What standard is Zigbee based on?** IEEE 802.15.4 (PHY + MAC). Zigbee adds the network and application layers.
2. **What frequency and data rate?** 2.4 GHz at 250 kbps (also 868/915 MHz).
3. **What are the three device types?** Coordinator, Router and End Device. There is only one coordinator per network.
4. **Why mesh?** Self-healing, longer range through multi-hop, and no single point of failure.
5. **What is a PAN ID?** A 16-bit ID that separates Zigbee networks. All nodes in a network share it.
6. **AT vs API mode?** AT/transparent mode is a raw serial pipe to a fixed destination. API mode uses structured frames with addressing, ACKs and RSSI.
7. **How does Zigbee save power?** End devices sleep and poll their parent. There's a low duty cycle and short frames.
8. **Security?** AES-128, with a network key, link keys and a Trust Center (the coordinator).
9. **Zigbee vs Bluetooth?** Zigbee uses less power, supports more nodes (65k vs 7) and supports mesh, but has a lower data rate.
10. **Why are DH=0, DL=0 on the router?** Address 0x0000 is always the coordinator.
11. **What is ZCL?** The Zigbee Cluster Library: standard clusters such as On/Off and Temperature, so devices from different vendors can work together.
12. **Which UART pins are on the Pi?** GPIO14 (TXD, pin 8) and GPIO15 (RXD, pin 10).
