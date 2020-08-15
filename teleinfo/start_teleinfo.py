from common.database.databasetype import DatabaseType
from models.settings import Settings, Logging

import sys

if __name__ == '__main__':
    settings = Settings.singleton()

    if settings.service_already_running():
        Logging.error("Service teleinfo is already running")
        sys.exit()

    open(settings.pidfile, 'w').write(settings.pid)

    try:
        Logging.info("Start Teleinfo application")
        settings.init_db(DatabaseType.SQLITE)

        # Creation of models
        import models
        from serial_teleinfo import teleinfo

        Logging.info("Check creation of tables")
        settings.database.init_tables()

        teleinfo.Teleinfo().run()
    finally:
        settings.dispose()

