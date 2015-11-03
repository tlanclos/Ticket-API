from flask.ext.sqlalchemy import SQLAlchemy
from ticketapi.apps import app


__all__ = ['Company', 'Session', 'Ticket']


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp_db.db'
db = SQLAlchemy(app)


class Company(db.Model):
    """
    Company table which holds company login information such as the pepper/salted/hashed password
    """
    companyID = db.Column(db.String(64), primary_key=True)
    companyName = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(16), unique=False, nullable=False)
    sessions = db.relationship('Session', backref='company', lazy='dynamic')


class Session(db.Model):
    """
    Session table which holds information about the employee. This will be used when an
    employee updates his or her information such as name, email, and phone number
    """
    authKey = db.Column(db.String(36), primary_key=True)
    firstName = db.Column(db.String(32), unique=False, nullable=True)
    lastName = db.Column(db.String(32), unique=False, nullable=True)
    email = db.Column(db.String(64), unique=False, nullable=True)
    phoneNumber = db.Column(db.String(32), unique=False, nullable=True)
    creationTime = db.Column(db.DateTime, unique=False, nullable=True)
    companyID = db.Column(db.String(64), db.ForeignKey('company.companyID'))
    tickets = db.relationship('Ticket', backref='session', lazy='dynamic')


class Ticket(db.Model):
    """
    Ticket table which holds information about a ticket submission such as the
    location, photo, and description
    """
    ticketID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024), unique=False, nullable=False)
    location = db.Column(db.String(64), unique=False, nullable=True)
    photo = db.Column(db.String(1024), unique=False, nullable=True)
    creationTime = db.Column(db.DateTime, unique=False, nullable=False)
    authKey = db.Column(db.String(36), db.ForeignKey('session.authKey'))
