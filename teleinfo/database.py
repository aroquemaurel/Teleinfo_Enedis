from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.db_prod import db_user, db_password, db_url, db_table


class Database:
    app = None
    db = None
    user = db_user
    password = db_password
    url = db_url
    table = db_table

    def __init__(self):
        self.init_db()

    def init_db(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                                     self.user + ':' + \
                                                     self.password + '@' + \
                                                     self.url + '/' +\
                                                     self.table
        self.db = SQLAlchemy(self.app)

    def init_tables(self):
        if self.db is not None:
            self.db.create_all()
            self.db.session.commit()

    def close(self):
        if self.db is not None:
            self.db.session.close()

    def commit_model(self, model):
        self.db.session.add(model)
        self.db.session.commit()
