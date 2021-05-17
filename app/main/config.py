import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "mongodb://127.0.0.1:27017/flask_dev_db"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = "mongodb://127.0.0.1:27017/flask_test_db"


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = "mongodb://127.0.0.1:27017/flask-app"


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
