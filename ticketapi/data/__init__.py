import json

__version__ = '0.0.1'
__all__ = ['fields', 'response', 'logger', 'validators', 'decorators']


SETTINGS_FILE = '/var/www/html/ticketapi/settings.json'
LOG_FILE = '/var/log/ticket-api/ticket-api.log'

with open(SETTINGS_FILE, 'r') as settings:
    SETTINGS = json.loads(settings.read())
