# Zigbee: Theory and How to Set It Up

**Platform:** 2 × Raspberry Pi, each with a Digi XBee S2C (Zigbee) module on a USB Explorer (serial/COM port `/dev/ttyUSB0`), XCTU for configuration, and Python `pyserial`.
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

- 2 × **Raspberry Pi** (3B+/4) running Raspberry Pi OS: Pi A is the Coordinator and Pi B is the Router
- 2 × **Digi XBee S2C** (Zigbee 3.0) modules (Series 1 XBee modules are plain 802.15.4, *not* Zigbee)
- 2 × **XBee USB Explorer** boards. Each XBee plugs into a Pi's USB port and shows up as a serial (COM) port, `/dev/ttyUSB0`
- 1 × LED + 220 Ω resistor on the router Pi: GPIO18 (pin 12) → 220 Ω → LED long leg, and the short leg → GND (pin 6)
- A laptop with **XCTU** (free from Digi), used once to configure both XBees

```
 Pi A (Coordinator)                         Pi B (Router)
 +--------------+   USB   +-------+  2.4 GHz  +-------+   USB   +--------------+
 | coordinator  |========>| XBee  | ))) ((( | XBee  |========>| router.py    |---> GPIO18 LED
 |    .py       |ttyUSB0  | CE=1  |  Zigbee   | CE=0  | ttyUSB0 |              |
 +--------------+         +-------+           +-------+         +--------------+
```

## 8. Step 1: Configure both XBees in XCTU (on a laptop)

Plug an XBee on its USB Explorer into the laptop and open **XCTU**. Click **Add device**, pick its COM port (Device Manager → Ports shows COM3 or similar), keep 9600 baud, and click Finish. Do this for each module.

If a module has the wrong firmware, click **Update firmware**, choose product family **XB24C**, and pick the function set **Zigbee Coordinator AT** for one module and **Zigbee Router AT** for the other. On newer S2C firmware ("Zigbee TH Reg"), one firmware covers both roles and **CE** decides the role.

| Parameter | Coordinator XBee | Router XBee | Meaning |
|---|---|---|---|
| **ID** (PAN ID) | `1234` | `1234` | **Must match.** This is how the router finds the coordinator's network |
| **CE** (Coordinator Enable) | `1` (Enabled) | `0` (Disabled) | Exactly one coordinator |
| **JV** (Channel Verification) | – | `1` | Router checks that the coordinator exists and rejoins if it doesn't |
| **DH** (Destination High) | `0` | `0` | DH + DL = who to send to |
| **DL** (Destination Low) | `FFFF` (broadcast) | `0` | Coordinator broadcasts to everyone. Router's `0` = "send to the coordinator" |
| **BD** (Baud rate) | `3` = 9600 | `3` = 9600 | Must match `baudrate=9600` in Python |
| **AP** (API mode) | `0` = Transparent | `0` = Transparent | Plain serial pipe. Our code uses this |
| **NI** (Node Identifier) | `COORD` | `ROUTER` | Label shown in XCTU |

Click **Write** (the pencil icon) after changing the values on each module.

Instead of broadcasting, the coordinator can send to the router only. To do that, set the coordinator's **DH = router's SH** and **DL = router's SL**. SH/SL is the 64-bit address printed on the back of the router XBee and shown in XCTU.

## 9. Step 2: How the router connects (joins) to the coordinator

This is what happens over the air when both are powered:

1. **Coordinator starts the network.** It scans the channels (11–26), picks a quiet one, and forms a PAN with ID `1234`. It becomes address **0x0000**. Its **Associate LED** starts blinking.
2. **Router scans for networks.** It sends **beacon requests** on each channel.
3. **Coordinator replies with a beacon**, which carries its PAN ID and says it allows joining.
4. **Router matches the PAN ID.** The ID in the beacon (`1234`) equals the router's own **ID**, so it sends an **association request**.
5. **Coordinator accepts.** It sends an **association response** and gives the router a 16-bit network address (**MY**, e.g. `0x3A7F`). With security on, it also sends the network key, because the coordinator acts as Trust Center.
6. **Joined.** The router's Associate LED starts blinking, and its **AI** (Association Indication) reads **`0`**, which means joined successfully.
7. **Data flows.** The router's DH/DL of `0/0` routes its data to the coordinator. The coordinator's broadcast (`FFFF`) reaches the router.

### How to check they're connected

- **Associate LED** on both XBees blinks (about once per second). A solid light means not joined.
- In XCTU, read **AI** on the router. **`0`** means joined. Other values mean it's still scanning or failed.
- In XCTU, read **OP** (Operating PAN ID). It should be the same 64-bit value on both modules.
- On the router, **MY** is not `FFFE`, so it has a network address.
- In XCTU's **Network** view (the globe icon), scan from the coordinator. You should see COORD linked to ROUTER.
- **Console test**: open the XCTU console on both modules (two laptops, or two Explorers on one laptop). Text typed on one appears on the other.

Once this works, close XCTU, unplug the XBees from the laptop, and plug each one into its Pi.

## 10. Step 3: Set up both Raspberry Pis

```bash
ls /dev/ttyUSB*               # XBee shows as /dev/ttyUSB0 (the Pi's "COM port")
python3 find_com_ports.py     # same thing, with descriptions
sudo usermod -aG dialout $USER   # allow serial access without sudo, then log out/in
pip3 install pyserial         # usually preinstalled
```

If the port isn't `/dev/ttyUSB0`, change `PORT` at the top of the script.

## 11. Step 4: Run

Power on the **coordinator first**, then the router, and wait about 5 s for the Associate LEDs to blink.

```bash
# Pi B (router / receiver) - start first so nothing is missed
python3 zigbee_router.py
# Pi A (coordinator / transmitter)
python3 zigbee_coordinator.py
```

### Expected output

Coordinator (Pi A):
```
Zigbee Coordinator (Transmitter) Initialized on Raspberry Pi (/dev/ttyUSB0)...
[TX Packet #1] Sent -> CMD:ON|TEMP:29.0
[TX Status] Sent -> CMD:OFF|TEMP:28.0
```
Router (Pi B):
```
Zigbee Router/End-Device (Receiver) Ready on Raspberry Pi (/dev/ttyUSB0)...
[RX Zigbee Frame] Received: CMD:ON|TEMP:29.0
 -> Actuator State: GPIO18 HIGH (LED TURNED ON)
[RX Zigbee Frame] Received: CMD:OFF|TEMP:28.0
 -> Actuator State: GPIO18 LOW (LED TURNED OFF)
```
The LED on Pi B blinks ON and OFF every 2 s.

## 12. How the code works

- `serial.Serial('/dev/ttyUSB0', 9600)` opens the serial (COM) port that the XBee's USB Explorer creates.
- The **Coordinator** builds a text frame `CMD:ON|TEMP:x` and calls `.encode()` to turn it into bytes. `zigbee.write()` hands them to the XBee, and the XBee transmits them over 2.4 GHz to DH/DL.
- The **Router's** XBee receives the RF packet and outputs it on its serial port. `in_waiting > 0` checks whether bytes have arrived, then `readline()` reads up to `\n`.
- `startswith("CMD:ON")` parses the command and sets `GPIO.output(18, HIGH/LOW)`.
- `\n` is the frame delimiter. `try/except KeyboardInterrupt` closes the port and runs GPIO cleanup.

## 13. Troubleshooting

| Problem | Fix |
|---|---|
| Router's Associate LED is solid (not blinking) | It hasn't joined. Check that the **ID** values match, that only one module has **CE=1**, and that the coordinator was powered first. Check the router's **AI** in XCTU |
| Joined but nothing received | The router's **DL** must be `0`. The coordinator's **DL** must be `FFFF` or the router's SL |
| Garbage characters | The baud rate in XCTU (BD) doesn't match the code |
| `could not open port /dev/ttyUSB0` | Wrong port (run `ls /dev/ttyUSB*`), or no permission (`dialout` group / `sudo`) |
| Port busy | XCTU or another script has it open. Close it |

## 14. Alternative platforms (if asked "how else can Zigbee be done?")

- **Arduino/ESP32 + XBee**: same XCTU setup. Use `SoftwareSerial` or `Serial2` and `Serial.print("CMD:ON")`.
- **XBee API mode (AP=1/2) + `digi-xbee` Python library**: structured frames with source address, RSSI and checksum, plus remote AT commands. Code looks like `XBeeDevice("/dev/ttyUSB0", 9600).send_data_broadcast("hello")`.
- **Zigbee2MQTT / Home Assistant**: a USB Zigbee coordinator dongle (e.g. Sonoff ZBDongle, CC2652) on a PC or Pi bridges commercial Zigbee bulbs and sensors to MQTT topics. This ties Zigbee and MQTT together.
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
12. **What is a COM port?** A serial port. The USB Explorer's FTDI chip converts USB to UART, so the Pi sees the XBee as `/dev/ttyUSB0` and Windows sees it as `COMx`. `pyserial` opens it like a file.
13. **How does the router join the coordinator?** It sends beacon requests, finds a beacon with a matching PAN ID, sends an association request, and gets a 16-bit address from the coordinator. After that AI = 0 and the Associate LED blinks.
