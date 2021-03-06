from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myapp.config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_share import Share
from .celery_utils import init_celery
import os




db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
ckeditor=CKEditor()
migrate=Migrate()
admin=Admin()
share=Share()


PKG_NAME=os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

def create_app(config_class=Config, app_name=PKG_NAME, **kwargs):
    Myapp=Flask(app_name)
    Myapp.config.from_object(Config)
    

    #print(Myapp.config)
    
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), Myapp)

    from myapp.models import MyAdminIndexView, File
    db.init_app(Myapp)
    bcrypt.init_app(Myapp)
    login_manager.init_app(Myapp)
    mail.init_app(Myapp)
    admin.init_app(Myapp, index_view=MyAdminIndexView())
    ckeditor.init_app(Myapp)
    migrate.init_app(Myapp, db)
    share.init_app(Myapp)
    
    

    from myapp.users.routes import users
    from myapp.posts.routes import posts
    from myapp.main.routes import main
    from myapp.errors.handlers import errors
    from myapp.comments.routes import comments
    from myapp.files.routes import files
    from myapp.models import MyAdminIndexView
    Myapp.register_blueprint(users)
    Myapp.register_blueprint(posts)
    Myapp.register_blueprint(main)
    Myapp.register_blueprint(errors)
    Myapp.register_blueprint(comments)
    Myapp.register_blueprint(files) 
    return Myapp
