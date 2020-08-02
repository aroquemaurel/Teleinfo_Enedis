import sys

from serial import Serial, PARITY_NONE, STOPBITS_ONE, SEVENBITS

import models
from Keywords import Keyword
from settings import Settings, Logging


class Teleinfo():
    serial = None
    settings = Settings.singleton()

    def run(self):
        nb_error = 0
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
                key = Keyword.value_of(ar[0])
                if key is None:
                    line = self.read_line()
                    continue

                if key == Keyword.ADCO:  # Begining of block
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

                if key.is_int_value():
                    value = int(ar[1])
                else:
                    value = ar[1]

                if key == Keyword.HCHP:
                    consumption.index_hp = value
                elif key == Keyword.HCHC:
                    consumption.index_hc = value
                elif key == Keyword.IINST:
                    consumption.intensite_inst = value
                elif key == Keyword.PAPP:
                    consumption.puissance_apparente = value
                elif key == Keyword.PTEC:
                    if value == "HC..":
                        consumption.periode = 2

                self.settings.remove_error_file()
                nb_error = 0
            except Exception as e:
                nb_error = nb_error + 1
                if nb_error > 20:
                    sys.exit()

                try:
                    Logging.error("Exception : %s" % e)
                    self.settings.create_error_file()
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
