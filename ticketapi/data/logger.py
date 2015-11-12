from ticketapi.data import LOG_FILE
import logging
import logging.config

__all__ = ['logger']

log_settings = {
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': LOG_FILE,
            'mode': 'a',
            'maxBytes': 2621440,
            'backupCount': 9,
        },

    },

    'loggers': {
        'API-basic': {
            'level': 'INFO',
            'handlers': ['file']
        }
    }
}

logging.config.dictConfig(log_settings)

logger = logging.getLogger('API-basic')


if __name__ == '__main__':
    for i in range(50):
        logger.info('test' + str(i))
