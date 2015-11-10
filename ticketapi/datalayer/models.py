from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from urllib import parse
from ticketapi.apps import app
from ticketapi.data import SETTINGS

__all__ = ['Company', 'Session', 'Ticket']

connection_string = "DRIVER={dsn};UID={username};PWD={password}".format(
    dsn=SETTINGS['db_dsn'],
    username=SETTINGS['db_username'],
    password=SETTINGS['db_password']
)
connection_string = parse.quote_plus(connection_string)
connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)

metadata = MetaData()

metadata.reflect(db.engine, schema='ticketapi')

Base = automap_base(metadata=metadata)
Base.prepare()

Company = Base.classes.Authentication
Session = Base.classes.Session
Ticket = Base.classes.Ticket
