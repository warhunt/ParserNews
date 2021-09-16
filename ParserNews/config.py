from os import environ, getenv
from logging import DEBUG as log_debug

class ConfigFactory(object):
    def factory():
        env = environ.get("APP_SETTINGS", "Dev")
        conf = {
            'Dev': DevelopmentConfig(),
            'Prod': ProductionConfig()
        }

        return conf.get(env)

class Config:

    URL_WEBSITE=environ.get('URL_WEBSITE')

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    DB = getenv('DB')
    HOST = getenv('HOST')

    #variables for logging the application
    LOGGER_NAME = environ.get("LOGGER_NAME", "logger")
    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': "[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s",
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': f"{LOGGER_NAME}.log",
            },
        },
        'loggers': {
            LOGGER_NAME: {
                'handlers': ['file', ],
                'level': log_debug
            },
        },
    }

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    pass
