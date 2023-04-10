

from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# class GPSdata(db.Model, UserMixin):

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())



class Flightmaster(db.Model): 
    __tablename__ = 'flightmaster'
    id = db.Column(db.Integer, primary_key=True)
    loginId = db.Column(db.Integer, db.ForeignKey('user.id'))

    startTime = db.Column(db.String(200))
    endTime = db.Column(db.String(200))

    #gpsRelation = db.relationship('GPSdata')
    #telemRelation = db.relationship('telemData')


class GPSdata(db.Model):
    __tablename__ = 'gpsdata'
    id = db.Column(db.Integer, primary_key=True)
    flightId = db.Column(db.Integer, db.ForeignKey("flightmaster.id"))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    lat = db.Column(db.Float(150))
    lon = db.Column(db.Float(150))



class Telemdata(db.Model):
    __tablename__ = 'telemdata'
    id = db.Column(db.Integer, primary_key=True)
    flightId = db.Column(db.Integer, db.ForeignKey("flightmaster.id"))
    time = db.Column(db.DateTime(timezone=True), default=func.now())

    temperature = db.Column(db.Float(60))
    pressure = db.Column(db.Float(60))
    humidity = db.Column(db.Float(60))

    gas = db.Column(db.Float(60))
    co2 = db.Column(db.Float(60))
    tvoc = db.Column(db.Float(60))

    flightTime = db.Column(db.Float(150))









    