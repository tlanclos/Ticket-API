__all__ = ['logger']

import logging.config


log_settings = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'ticket-api.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 20,
        },

    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    'loggers': {
        'API-basic': {
            'level': 'INFO',
            'handlers': ['file']
            }
        }
    }
}

logging.config.dictConfig(log_settings)

logger = logging.getLogger('API-basic')

