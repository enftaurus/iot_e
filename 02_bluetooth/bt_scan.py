import subprocess

# Discover nearby Bluetooth devices (handy first step / viva demo).
# Uses bluetoothctl, which ships with Raspberry Pi OS.

print("Scanning for Bluetooth devices for 10 seconds...")
subprocess.run(["bluetoothctl", "--timeout", "10", "scan", "on"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

out = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True).stdout
devices = [line.split(" ", 2) for line in out.splitlines() if line.startswith("Device")]

print(f"Found {len(devices)} device(s):")
for _, mac, name in devices:
    print(f"  {mac}  ->  {name}")
