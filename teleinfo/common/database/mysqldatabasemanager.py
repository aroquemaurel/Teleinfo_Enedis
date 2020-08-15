from abc import abstractmethod

from common.database.databasemanager import DatabaseManager
from config.db_prod import db_user, db_password, db_url, db_table


class MySQLDatabaseManager(DatabaseManager):
    user = db_user
    password = db_password
    url = db_url
    table = db_table

    @property
    def uri(self):
        return 'mysql+mysqlconnector://' + self.user + ':' + self.password + '@' + self.url + '/' + self.table