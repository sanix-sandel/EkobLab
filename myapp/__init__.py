import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


Myapp=Flask(__name__)
Myapp.config['SECRET_KEY']='842551071e8a5f7a16f9029e37863f4a'
Myapp.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(Myapp)
bcrypt=Bcrypt(Myapp)
login_manager = LoginManager(Myapp)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
Myapp.config['MAIL_SERVER'] = 'smtp.googlemail.com'
Myapp.config['MAIL_PORT'] = 587
Myapp.config['MAIL_USE_TLS'] = True
Myapp.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
Myapp.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(Myapp)

from myapp.users.routes import users
from myapp.posts.routes import posts
from myapp.main.routes import main

Myapp.register_blueprint(users)
Myapp.register_blueprint(posts)
Myapp.register_blueprint(main)

