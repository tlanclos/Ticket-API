from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from urllib import parse
from ticketapi.apps import app
from ticketapi.data import SETTINGS_FILE

__all__ = ['Company', 'Session', 'Ticket']

connection_string = "DRIVER={{SQL Server}};Database={0};SERVER={1};UID={2};PWD={3}".format(
    SETTINGS_FILE['db_name'],
    SETTINGS_FILE['db_server'],
    SETTINGS_FILE['db_username'],
    SETTINGS_FILE['db_password']
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

