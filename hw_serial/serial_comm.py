# serial/serial_comm.py
import serial
import serial.tools.list_ports

class SerialCommunicator:
    def __init__(self):
        self.ser = None

    def list_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    @property
    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def connect(self, port, baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            return True
        except Exception:
            self.ser = None
            return False

    def disconnect(self):
        if self.ser:
            self.ser.close()
        self.ser = None

    def send_hex(self, hex_str):
        if not self.is_connected:
            return False
        try:
            clean = hex_str.replace("0x", "").replace(" ", "")
            self.ser.write(bytes.fromhex(clean))
            return True
        except Exception:
            return False
