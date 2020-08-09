from databasemanager import DatabaseManager
from mysqldatabasemanager import MySQLDatabaseManager
from settings import Settings

global db
if __name__ == '__main__':
    sqlite_db = DatabaseManager()
    mysql_db = MySQLDatabaseManager()

    try:
        sqlite_db.init_db()
        mysql_db.init_db()

        Settings.singleton().database = mysql_db
        from models import Consumption
        max_id = mysql_db.db.session.query(mysql_db.db.func.max(Consumption.id)).scalar()
        if max_id is None:
            max_id = 0

        Settings.singleton().database = sqlite_db 
        from models import Consumption
        data_to_insert = sqlite_db.db.session.query(Consumption).filter(Consumption.id > max_id).all()
        for data in data_to_insert:
            consumption = Consumption()
            consumption.id = data.id
            consumption.datetime = data.datetime
            consumption.periode = data.periode
            consumption.index_hp = data.index_hp
            consumption.index_hc = data.index_hc
            consumption.intensite_inst = data.intensite_inst
            consumption.puissance_apparente = data.puissance_apparente
            mysql_db.db.session.add(consumption)

        mysql_db.db.session.commit()

    finally:
        sqlite_db.close()
        mysql_db.close()

    


