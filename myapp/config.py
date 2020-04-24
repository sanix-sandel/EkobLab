import os


class Config:
    
    SECRET_KEY='842551071e8a5f7a16f9029e37863f4a'#os.environ.get('SECRET_KEY')#
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'  
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SIMPLEMDE_jS_IIFE=True
    SIMPLEMDE_USE_CDN=True
    EKO_MAIL_SUBJECT_PREFIX='[EKOB]'
    EKO_MAIL_SENDER='techyintelo@gmail.com'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_BROKER_URL='amqp://localhost//'
    CELERY_RESULT_BACKEND='amqp://localhost//'
   

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
