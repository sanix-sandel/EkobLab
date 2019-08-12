from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myapp.config import Config


db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    Myapp=Flask(__name__)
    Myapp.config.from_object(Config)

    db.init_app(Myapp)
    bcrypt.init_app(Myapp)
    login_manager.init_app(Myapp)
    mail.init_app(Myapp)

    from myapp.users.routes import users
    from myapp.posts.routes import posts
    from myapp.main.routes import main
    from myapp.errors.handlers import errors
    Myapp.register_blueprint(users)
    Myapp.register_blueprint(posts)
    Myapp.register_blueprint(main)
    Myapp.register_blueprint(errors)


    return Myapp
