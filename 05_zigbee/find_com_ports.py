from serial.tools import list_ports

# Lists all serial (COM) ports - shows which /dev/ttyUSBx (Pi) or COMx (Windows) the XBee is on.
ports = list(list_ports.comports())
if not ports:
    print("No serial ports found. Check the XBee USB Explorer cable.")
for p in ports:
    print(f"{p.device}  ->  {p.description}")
