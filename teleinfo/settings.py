from config.prod import db_user, db_password, db_url, db_table
import logging

class Settings:
    __instance__ = None
    app = None
    db = None
    user = db_user
    password = db_password
    url = db_url
    table = db_table
    serial_dev = "/dev/ttyAMA0"
    log_file = '/var/log/teleinfo/releve.log'

    def __init__(self):
        # TODO : if /var/log/teleinfo does not exists...
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Teleinfo starting..")

    @staticmethod
    def singleton():
        if Settings.__instance__ is None:
            Settings.__instance__ = Settings()

        return Settings.__instance__


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
        print (msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)
        print(msg)
