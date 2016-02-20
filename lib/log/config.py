import sys


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    'filters': {
        'slack_only': {
            '()': 'lib.log.slack.SlackLogFilter'
        }
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': sys.stdout,
        },
        'slack': {
            'class': 'lib.log.slack.SlackLogHandler',
            'level': 'SLACK',
            'filters': ['slack_only'],
            'formatter': 'simple'
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
            'handlers': ['console', 'slack']
        },
    }
}
