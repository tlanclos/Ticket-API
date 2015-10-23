__all__ = ['logger']

import logging.config


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
            'filename': 'ticket_API.log',
            'mode': 'a',
            'maxBytes': 25600,
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


"""def main():
    for i in range(50):
        logger.info("test" + str(i))


if __name__ == "__main__":
    main()"""