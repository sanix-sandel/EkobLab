import os



class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')#'842551071e8a5f7a16f9029e37863f4a'
    SQLALCHEMY_DATABASE_URI= 'postgresql://sanix:19972017Russia@localhost/db'#'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


#ici
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True