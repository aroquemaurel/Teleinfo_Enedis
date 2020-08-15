from abc import abstractmethod

from common.database.databasemanager import DatabaseManager
from config.config import config_dev

if config_dev:
    from config.db_prod_mysql import *
else:
    from config.db_dev_mysql import *


class MySQLDatabaseManager(DatabaseManager):
    user = db_user
    password = db_password
    url = db_url
    table = db_table

    @property
    def uri(self):
        return 'mysql+mysqlconnector://' + self.user + ':' + self.password + '@' + self.url + '/' + self.table