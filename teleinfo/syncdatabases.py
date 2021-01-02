from common.database.mysqldatabasemanager import MySQLDatabaseManager
from common.database.sqlitedatabasemanager import SQLiteDatabaseManager 
from models.settings import Settings
from config.config import *

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
        from models.settings import Logging
        max_id = mysql_db.db.session.query(mysql_db.db.func.max(models.Consumption.id)).scalar()
        Logging.info("max_id : "+str(max_id))
        if max_id is None:
            max_id = 0

        Settings.singleton().database = sqlite_db 
        from models import models 
        data_to_insert_query = sqlite_db.db.session.query(models.Consumption).filter(models.Consumption.id > max_id)
        nb_entry = data_to_insert_query.count()
        Logging.info("Synchronize "+str(nb_entry)+" values")

        for i in range(nb_entry % config_nb_values_trame):
            range_from = i * config_nb_values_trame 
            range_to = (i + 1) * config_nb_values_trame 
            Logging.info("Synchronize data from "+str(range_from) + " to "+str(range_to))
            data_to_insert = data_to_insert_query.slice(range_from, range_to).all()

            for data in data_to_insert:
                consumption = models.Consumption(data)
                last_insert = consumption.id
                mysql_db.db.session.add(consumption)

            mysql_db.db.session.commit()

    finally:
        sqlite_db.close()
        mysql_db.close()

    


