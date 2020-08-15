import os
from abc import abstractmethod

from common.database.databasemanager import DatabaseManager
from config.db_prod_sqlite import db_sqlite_base_path


class SQLiteDatabaseManager(DatabaseManager):
    @property
    def uri(self):
        dir = os.path.dirname(db_sqlite_base_path)
        db_path = db_sqlite_base_path
        if not os.path.isdir(dir):
            db_path = __file__ + "/teleinfo.sqlite.db"

        return 'sqlite:////' + db_path


