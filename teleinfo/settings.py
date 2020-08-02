from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.prod import db_user, db_password, db_url, db_table
import logging
import os
import sys

class Settings:
    __instance__ = None
    app = None
    db = None
    user = db_user
    password = db_password
    url = db_url
    table = db_table
    serial_dev = "/dev/ttyAMA0"
    log_file = '/var/logs/pi/teleinfo.log'
    pidfile = "/tmp/teleinfo.pid"
    pid = str(os.getpid())

    def __init__(self):
        # TODO : if /var/log/teleinfo does not exists...
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info("Teleinfo starting..")

    @staticmethod
    def singleton():
        if Settings.__instance__ is None:
            Settings.__instance__ = Settings()

        return Settings.__instance__

    def service_already_running(self):
        return os.path.isfile(self.pidfile)

    def dispose(self):
        os.unlink(self.pidfile)
        self.db.session.close()

    def init_db(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://'+self.user+':'+self.password+'@'+self.url+'/'+self.table
        self.db = SQLAlchemy(self.app)

    def init_tables(self):
        self.db.create_all()
        self.db.session.commit()



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
