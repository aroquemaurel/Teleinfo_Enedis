import datetime
from settings import Settings


db = Settings.singleton().database.db


class Consumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    periode = db.Column(db.Integer, default=1) #1 => HP, 2 => HC
    index_hp = db.Column(db.Integer)
    index_hc = db.Column(db.Integer)
    intensite_inst = db.Column(db.Integer)
    puissance_apparente = db.Column(db.Integer)

    def __init__(self):
        self.datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=2) 

    def has_same_characteristics_as(self, other):
        return self.has_same_indexes(other) and self.periode == other.periode and self.intensite_inst == other.intensite_inst and self.puissance_apparente == other.puissance_apparente

    def has_same_indexes(self, other):
        return self.index_hp == other.index_hp and self.index_hc == other.index_hc


# This is for options that normally not change across time
class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow()+datetime.timedelta(hours=3))
    iMax = db.Column(db.Integer)
    intensite_souscrite = db.Column(db.Integer)
    horaires_hp_hc = db.Column(db.String(16))
    optarif = db.Column(db.String(16))

