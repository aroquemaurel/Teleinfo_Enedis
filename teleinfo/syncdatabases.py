from common.database.mysqldatabasemanager import MySQLDatabaseManager
from common.database.sqlitedatabasemanager import SQLiteDatabaseManager 
from models.settings import Settings

global db

"""
Synchronize the local database (sqlite) with the remote database (mysql). 
"""
if __name__ == '__main__':
    sqlite_db = SQLiteDatabaseManager()
    mysql_db = MySQLDatabaseManager()

    try:
        sqlite_db.init_db()
        mysql_db.init_db()

        Settings.singleton().database = mysql_db
        from models import models 
        max_id = mysql_db.db.session.query(mysql_db.db.func.max(models.Consumption.id)).scalar()
        if max_id is None:
            max_id = 0

        Settings.singleton().database = sqlite_db 
        from models import models 
        data_to_insert = sqlite_db.db.session.query(models.Consumption).filter(models.Consumption.id > max_id).all()
        for data in data_to_insert:
            consumption = models.Consumption(data)
            mysql_db.db.session.add(consumption)

        mysql_db.db.session.commit()

    finally:
        sqlite_db.close()
        mysql_db.close()

    


