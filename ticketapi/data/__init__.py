import os
import json

__version__ = '0.1.0'
__all__ = ['fields', 'response', 'logger', 'validators', 'decorators']


# Common variables for file locations
TICKET_API_ROOT = '/var/www/html/ticketapi'
SETTINGS_FILE = os.path.join(TICKET_API_ROOT, 'settings.json')
LOG_FILE = '/var/log/ticket-api/ticket-api.log'

# Open the file and read it's json contents into SETTINGS
with open(SETTINGS_FILE, 'r') as settings:
    SETTINGS = json.loads(settings.read())
