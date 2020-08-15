from serial import Serial, PARITY_NONE, STOPBITS_ONE, SEVENBITS

from models.settings import Settings, Logging


class SerialManager:
    serial = None
    settings = Settings.singleton()

    def __init__(self):
        self.serial = Serial(port=self.settings.serial_dev,
                             baudrate=1200,
                             parity=PARITY_NONE,
                             stopbits=STOPBITS_ONE,
                             bytesize=SEVENBITS,
                             timeout=1)
        Logging.info("Teleinfo is reading on " + self.settings.serial_dev + "...")

        Logging.info("Search the beginning of the trame")
        self.search_beginning_trame()

    def search_beginning_trame(self):
        line = self.serial.readline()
        while b'\x02' not in line:  # search the beginning trame character
            line = self.serial.readline()

    def read_line(self):
        return self.serial.readline().decode("utf-8")

    def close(self):
        self.serial.close()
        self.serial = None
