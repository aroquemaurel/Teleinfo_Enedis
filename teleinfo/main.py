from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Settings

if __name__ == '__main__':
    settings = Settings.singleton()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://'+settings.user+':'+settings.password+'@'+settings.url+'/'+settings.table
    db = SQLAlchemy(app)

    settings.app = app
    settings.db = db

    import models
    import teleinfo

    db.create_all()
    db.session.commit()

    teleinfo.main()
#    conso = models.Consumption(1, 2, 3, 4, 5)
#    db.session.add(conso)
#    db.session.commit()
