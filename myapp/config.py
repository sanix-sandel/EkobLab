import os



class Config:
    SECRET_KEY='842551071e8a5f7a16f9029e37863f4a'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')