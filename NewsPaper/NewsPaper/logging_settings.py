class LevelFilter(object):
    def __init__(self, level):
        self.level_name = level

    def filter(self, record) -> bool:
        return record.levelname == self.level_name


logging_params = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] - %(asctime)s - %(message)s',
        },
        'detailed': {
            'format': '[%(levelname)s] - "%(pathname)s" - %(asctime)s - %(message)s'
        },
        'file_detailed': {
            'format': '[%(levelname)s] - %(module)s - %(asctime)s - %(message)s'
        },
        'advanced': {
            'format': '[%(levelname)s] - "%(pathname)s" - %(asctime)s - %(exc_info)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'debug_level': {
            '()': 'NewsPaper.logging_settings.LevelFilter',
            'level': 'DEBUG',
        },
        'info_level': {
            '()': 'NewsPaper.logging_settings.LevelFilter',
            'level': 'INFO',
        },
        'warning_level': {
            '()': 'NewsPaper.logging_settings.LevelFilter',
            'level': 'WARNING',
        },
        'error_level': {
            '()': 'NewsPaper.logging_settings.LevelFilter',
            'level': 'ERROR',
        },
        'critical_level': {
            '()': 'NewsPaper.logging_settings.LevelFilter',
            'level': 'CRITICAL',
        },

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'debug_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'console_detailed': {
            'level': 'WARNING',
            'filters': ['require_debug_true', 'warning_level'],
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        },
        'console_advanced': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'advanced'
        },
        'file': {
            'level': 'INFO',
            'filters': ['info_level'],
            'class': 'logging.FileHandler',
            'formatter': 'file_detailed',
            'filename': 'logging/general.log',
        },
        'file_advanced': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'advanced',
            'filename': 'logging/errors.log',
        },
        'security_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file_detailed',
            'filename': 'logging/security.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_detailed', 'console_advanced', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_advanced', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_advanced', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_advanced'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['file_advanced'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'propagate': False,
        },
    }
}
