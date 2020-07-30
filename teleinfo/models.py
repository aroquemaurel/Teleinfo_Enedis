import datetime
from settings import Settings

db = Settings.singleton().db


class Consumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())
    periode = db.Column(db.Integer, default=1) #1 => HP, 2 => HC
    index_hp = db.Column(db.Integer)
    index_hc = db.Column(db.Integer)
    intensite_inst = db.Column(db.Integer)
    puissance_apparente = db.Column(db.Integer)

    def __init__(self, periode, index_hp, index_hc, intensite_inst, puissance_apparente):
        self.periode = periode
        self.index_hp = index_hp
        self.index_hc = index_hc
        self.intensite_inst = intensite_inst
        self.puissance_apparente = puissance_apparente


# This is for options that normally not change across time
class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    iMax = db.Column(db.Integer)
    intensite_souscrite = db.Column(db.Integer)
    horaires_hp_hc = db.Column(db.String(16))
    optarif = db.Column(db.String(16))

