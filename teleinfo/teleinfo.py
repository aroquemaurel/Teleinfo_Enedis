import serial

from serial import Serial, PARITY_NONE, STOPBITS_ONE, SEVENBITS

import models
from settings import Settings, Logging


class Teleinfo():
    int_measure_keys = ['IMAX', 'HCHC', 'IINST', 'PAPP', 'ISOUSC', 'ADCO', 'HCHP']
    serial = None
    settings = Settings.singleton()

    def run(self):
        self.build_serial()
        self.search_beginning_trame()

        # lecture de la première ligne de la première trame
        line = self.read_line()

        consumption = None
        last_consumption = None
        while True:
            line_str = line.decode("utf-8")
            ar = line_str.split(" ")
            try:
                key = ar[0]
                if key == 'ADCO':  # Begining of block
                    if consumption is not None:
                        if last_consumption is None or not last_consumption.has_same_indexes(consumption) or (
                                consumption.datetime - last_consumption.datetime).seconds > 30:
                            Settings.singleton().db.session.add(consumption)
                            Settings.singleton().db.session.commit()

                        last_consumption = consumption

                    consumption = models.Consumption()
                elif consumption is None:
                    Logging.warning("We search the beginning of first trame")
                    line = self.read_line()
                    continue

                if key in self.int_measure_keys:
                    value = int(ar[1])
                else:
                    value = ar[1]

                if key == 'HCHP':
                    consumption.index_hp = value
                elif key == 'HCHC':
                    consumption.index_hc = value
                elif key == 'IINST':
                    consumption.intensite_inst = value
                elif key == 'PAPP':
                    consumption.puissance_apparente = value
                elif key == 'PTEC':
                    if value == "HC..":
                        consumption.periode = 2

            except (AttributeError, MySQLdb.OperationalError) as e:
                if self.settings.db is not None:
                    self.settings.db.session.close()

                self.settings.init_db()
            except Exception as e:
                Logging.error("Exception : %s" % e)

            line = self.read_line()

        self.close_serial()

    def search_beginning_trame(self):
        line = self.read_line()
        while b'\x02' not in line:  # search the beginning trame character
            line = self.read_line()

    def build_serial(self):
        self.serial = Serial(port=Settings.singleton().serial_dev,
                             baudrate=1200,
                             parity=PARITY_NONE,
                             stopbits=STOPBITS_ONE,
                             bytesize=SEVENBITS, timeout=1)
        Logging.info("Teleinfo is reading on " + self.settings.serial_dev + "...")

    def read_line(self):
        return self.serial.readline()

    def close_serial(self):
        self.serial.close()
        self.serial = None
