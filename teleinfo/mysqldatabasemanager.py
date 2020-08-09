from databasemanager import DatabaseManager
from config.db_prod import db_user, db_password, db_url, db_table
from config.db_prod_sqlite import  db_sqlite_base_path

class MySQLDatabaseManager(DatabaseManager):
    user = db_user
    password = db_password
    url = db_url
    table = db_table

    def __init__(self):
        self.uri =  'mysql+mysqlconnector://' + self.user + ':' + self.password + '@' + self.url + '/' + self.table
