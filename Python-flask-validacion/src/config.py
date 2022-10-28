from secrets import token_hex
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or token_hex(16)
    TESTING = True
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/myDatabase'
    DEVELOPMENT = True
 


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}




