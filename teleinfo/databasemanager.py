from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.db_prod import db_user, db_password, db_url, db_table
from config.db_prod_sqlite import  db_sqlite_base_path


class DatabaseManager:
    app = None
    db = None

    uri = 'sqlite:////'+db_sqlite_base_path

    def init_db(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.uri
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
