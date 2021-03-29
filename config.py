import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecret')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIIONS', False)

    def init_app(self):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')


config = {"development": DevelopmentConfig, "production": ProductionConfig}
