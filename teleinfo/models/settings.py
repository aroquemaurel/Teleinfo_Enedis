import logging
import os

from common.database.databasetype import DatabaseType
from common.database.mysqldatabasemanager import MySQLDatabaseManager
from common.database.sqlitedatabasemanager import SQLiteDatabaseManager
from config.config import *


class Settings:
    __instance__ = None
    database = None
    serial_dev = config_serial_dev
    log_file = config_log_file
    pidfile = config_pidfile
    errorfile = config_errorfile
    pid = str(os.getpid())

    def __init__(self):
        if self.log_file is None or not os.path.isfile(self.log_file):
            self.log_file = "teleinfo.log"

        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Teleinfo starting..")

    def init_db(self, database_type):
        try:
            if self.database is not None:
                self.database.close()
        except Exception as e:
            Logging.error("Can't close existing database connection. %s" % e)

        if database_type == DatabaseType.SQLITE:
            Logging.info("Init SQLite database")
            self.database = SQLiteDatabaseManager()
        elif database_type == DatabaseType.MYSQL:
            Logging.info("Init MySQL database")
            self.database = MySQLDatabaseManager()

        self.database.init_db()

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
