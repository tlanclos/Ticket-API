from flask import Flask
from ticketapi.data.logger import logger

__version__ = '0.0.5'
__all__ = ['app']

app = Flask(__name__)
app.logger.addHandler(logger.handlers[0])
