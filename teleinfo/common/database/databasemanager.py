from abc import abstractmethod

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class DatabaseManager:
    app = None
    db = None

    @property
    @abstractmethod
    def uri(self):
        pass

    def init_db(self):
        from models.settings import Logging

        Logging.info("Init database with uri " + self.uri)
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
