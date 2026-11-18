from serial.tools import list_ports

# Lists all serial (COM) ports - shows which port the XBee is on.
ports = list(list_ports.comports())
if not ports:
    print("No serial ports found. Check the XBee cable / enable serial in raspi-config.")
for p in ports:
    print("{}  ->  {}".format(p.device, p.description))
