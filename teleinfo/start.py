
from settings import Settings, Logging

import logging
import sys

if __name__ == '__main__':
    settings = Settings.singleton()

    
    if settings.service_already_running():
        Logging.error("Service teleinfo is already running")
        sys.exit()

    open(settings.pidfile, 'w').write(settings.pid)

    try:
        Logging.info("Start Teleinfo application")


        Logging.info("Initialize MySQL database")
        settings.init_db()

        import models
        import teleinfo

        Logging.info("Check creation of tables")
        """ Create tables if needed """
        settings.init_tables()

        teleinfo.Teleinfo().run()
    finally:
        settings.dispose()

