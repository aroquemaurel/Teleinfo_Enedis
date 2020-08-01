from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Settings, Logging

import logging

if __name__ == '__main__':
    settings = Settings.singleton()
    Logging.info("Start Teleinfo application")

    app = Flask(__name__)

    Logging.info("Initialize MySQL database")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://'+settings.user+':'+settings.password+'@'+settings.url+'/'+settings.table
    db = SQLAlchemy(app)

    settings.app = app
    settings.db = db

    import models
    import teleinfo

    Logging.info("Check creation of tables")
    """ Create tables if needed """
    db.create_all()
    db.session.commit()

    teleinfo.Teleinfo().run()

