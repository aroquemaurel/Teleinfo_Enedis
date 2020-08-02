import sys

import models
from Keywords import Keyword
from serialmanager import SerialManager
from settings import Settings, Logging


class Teleinfo:
    serial_manager = None
    settings = Settings.singleton()
    database = settings.database

    def run(self):
        try:
            nb_error = 0
            self.serial_manager = SerialManager()

            # lecture de la première ligne de la première trame
            line = self.serial_manager.read_line()

            Logging.info("Reading data from teleinfo")
            consumption = None
            last_consumption = None
            while True:
                ar = line.split(" ")
                try:
                    key = Keyword.value_of(ar[0])
                    if key is None:
                        line = self.serial_manager.read_line()
                        continue

                    if key == Keyword.ADCO:  # Begining of block
                        if consumption is not None:
                            if last_consumption is None or not last_consumption.has_same_indexes(consumption) or (
                                    consumption.datetime - last_consumption.datetime).seconds > 30:
                                self.database.commit_model(consumption)
                                self.settings.remove_error_file()
                                nb_error = 0

                            last_consumption = consumption

                        consumption = models.Consumption()
                    elif consumption is None:
                        Logging.warning("We search the beginning of first trame")
                        line = self.serial_manager.read_line()
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

                except Exception as e:
                    nb_error = nb_error + 1
                    if nb_error > 20:
                        Logging.error("Too many error. Stop the service.")
                        sys.exit()

                    try:
                        Logging.error("Exception no "+str(nb_error)+": %s" % e)
                        self.settings.create_error_file()
                        self.settings.init_db()

                    except Exception as e2:
                        Logging.error("Exception : %s" % e2)

                line = self.serial_manager.read_line()
        finally:
            if self.serial_manager is not None:
                self.serial_manager.close()
                

