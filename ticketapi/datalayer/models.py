from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from urllib import parse
from ticketapi.apps import app
from ticketapi.data import SETTINGS

__all__ = ['Authentication', 'Session', 'Ticket']

# Get our connection string
connection_string = "DSN={dsn};UID={username};PWD={password}".format(
    dsn=SETTINGS['db_dsn'],
    username=SETTINGS['db_username'],
    password=SETTINGS['db_password']
)
connection_string = parse.quote_plus(connection_string)
connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string


# Set the app's connection string
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

# Tell SQLAlchemy to track modification of objects and emit signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# The connection recycle timeout is now 30 minutes
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800


db = SQLAlchemy(app)

metadata = MetaData()

metadata.reflect(db.engine, schema='ticketapi')

# Automagically map the database structure into Base
Base = automap_base(metadata=metadata)
Base.prepare()

# Declare the tables we'll need
Authentication = Base.classes.Authentication
Company = Base.classes.Company
Session = Base.classes.Session
Ticket = Base.classes.Ticket
