from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_example.db'
db = SQLAlchemy(app)


class Company(db.Model):
    companyID = db.Column(db.String(64), primary_key=True)
    companyName = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(16), unique=False, nullable=False)
    sessions = db.relationship('Session', backref='company', lazy='dynamic')

class Session(db.Model):
    authKey = db.Column(db.String(36), primary_key=True)
    firstName = db.Column(db.String(32), unique=False, nullable=True)
    lastName = db.Column(db.String(32), unique=False, nullable=True)
    email = db.Column(db.String(64), unique=False, nullable=True)
    phoneNumber = db.Column(db.String(32), unique=False, nullable=True)
    creationTime = db.Column(db.DateTime, unique=False, nullable=True)
    companyID = db.Column(db.String(64), db.ForeignKey('company.companyID'))
    tickets = db.relationship('Ticket', backref='session', lazy='dynamic')

class Ticket(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024), unique=False, nullable=False)
    location = db.Column(db.String(64), unique=False, nullable=True)
    photo = db.Column(db.String(1024), unique=False, nullable=True)
    creationTime = db.Column(db.DateTime, unique=False, nullable=False)
    authKey = db.Column(db.String(36), db.ForeignKey('session.authKey'))