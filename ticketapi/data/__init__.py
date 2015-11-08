import json

__version__ = '0.0.1'
__all__ = ['fields', 'response', 'logger', 'validators', 'decorators']


SETTINGS_FILE = json.loads(open('/var/www/html/ticketapi/settings.json').read())