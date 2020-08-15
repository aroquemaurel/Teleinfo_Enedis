import os

from common.database.databasemanager import DatabaseManager
from config.config import config_dev

if config_dev:
    from config.db_dev_sqlite import *
else:
    from config.db_prod_sqlite import *


class SQLiteDatabaseManager(DatabaseManager):
    @property
    def uri(self):
        dir = os.path.dirname(db_sqlite_base_path)
        db_path = db_sqlite_base_path
        if not os.path.isdir(dir):
            db_path = __file__ + "/teleinfo.sqlite.db"

        return 'sqlite:////' + db_path


