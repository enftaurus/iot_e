import subprocess

# Discover nearby Bluetooth devices (handy first step / viva demo).
# Uses bluetoothctl, which ships with Raspberry Pi OS.

print("Scanning for Bluetooth devices for 10 seconds...")
devnull = open("/dev/null", "w")
subprocess.call(["bluetoothctl", "--timeout", "10", "scan", "on"], stdout=devnull, stderr=devnull)

out = subprocess.check_output(["bluetoothctl", "devices"], universal_newlines=True)
devices = [line.split(" ", 2) for line in out.splitlines() if line.startswith("Device")]

print("Found {} device(s):".format(len(devices)))
for _, mac, name in devices:
    print("  {}  ->  {}".format(mac, name))
