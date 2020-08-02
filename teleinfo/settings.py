import logging
import os
from database import Database


class Settings:
    __instance__ = None
    database = None
    serial_dev = "/dev/ttyAMA0"
    log_file = '/var/log/pi/teleinfo.log'
    pidfile = "/tmp/teleinfo.pid"
    errorfile = "/tmp/teleinfo.error"
    pid = str(os.getpid())

    def __init__(self):
        # TODO : if /var/log/teleinfo does not exists...
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Teleinfo starting..")

    def init_db(self):
        if self.database is not None:
            self.database.close()

        self.database = Database()

    def service_already_running(self):
        return os.path.isfile(self.pidfile)

    def has_error(self):
        return os.path.isfile(self.errorfile)

    def dispose(self):
        os.unlink(self.pidfile)

        if self.has_error():
            os.unlink(self.errorfile)

        self.database.close()

    @staticmethod
    def singleton():
        if Settings.__instance__ is None:
            Settings.__instance__ = Settings()

        return Settings.__instance__

    def create_error_file(self):
        if not self.has_error():
            open(self.errorfile, 'w').write("")

    def remove_error_file(self):
        if self.has_error():
            os.unlink(self.errorfile)

    def database_is_init(self):
        return self.database is not None \
               and self.database.db is not None


class Logging:
    __instance__ = None

    @staticmethod
    def singleton():
        if Settings.__instance__ is None:
            Settings.__instance__ = Settings()

        return Settings.__instance__

    @staticmethod
    def info(msg):
        logging.info(msg)
        print(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)
        print(msg)
