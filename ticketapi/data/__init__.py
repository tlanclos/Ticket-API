import json

__version__ = '0.0.1'
__all__ = ['fields', 'response', 'logger', 'validators', 'decorators']


SETTINGS_FILE = '/var/www/html/ticketapi/settings.json'

with open(SETTINGS_FILE, 'r') as settings:
    SETTINGS = json.loads(settings.read())
