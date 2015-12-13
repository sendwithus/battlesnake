import logging
import logging.config
import sys


LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': sys.stdout,
        },
    },
    'formatters': {
        'simple': {
            'format': '%(message)s',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
}


logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(module_name):
    return logging.getLogger(module_name)
