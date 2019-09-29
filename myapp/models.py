from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from myapp import db, login_manager, admin, bcrypt
from flask import current_app, flash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.form import rules
from wtforms import widgets,TextAreaField, PasswordField


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)
    location=db.Column(db.String(30), nullable=True)  #ici
    comment=db.relationship('Comment', backref='author', lazy=True)
    files=db.relationship('File', backref='uploader',lazy=True)
    aboutme=db.Column(db.Text, nullable=True)
    admin=db.Column(db.Boolean())
    
    

    def is_admin(self):
        return self.admin

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User ('{self.username}','{self.email}', '{self.image_file}')"   

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)   
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.UnicodeText, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment=db.relationship('Comment', backref='post_comments', lazy='dynamic')
    _reads=db.Column(db.Integer, default=0)
    reads=_reads
    nbcomments=db.Column(db.Integer, default=0)

    extend_existing=True

    def _set_read(self, reads):
        self._reads=reads

    def nbrcomments(self):
        self.nbcomments+=1

    _reads=property(_set_read)    


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)  
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)



class File(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)   
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data=db.Column(db.LargeBinary, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    cover=db.Column(db.String(20), nullable=False, default='default.jpg')
    downloaded=db.Column(db.Integer, default=0)
   
    extend_existing=True

    def downloads(self):
        self.downloaded+=1
    

    def __repr__(self):
        return f"File('{self.title}', '{self.date_posted}')"    

class MyAdminIndexView(AdminIndexView): #availability of admin home page //admin=Admin(Myapp, index_view=admin.MyAdminindexView())
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget=CKTextAreaWidget()        


class PostView(ModelView):
    form_overrides=dict(content=CKTextAreaField)
    column_searchable_list=('title', 'content')
    

    create_template='new.html'
    edit_template='new.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class CommentView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class FilesView(ModelView):
    column_exclude_list = ('data',)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin        

class UserAdminView(ModelView):
    column_searchable_list=('username',)
    column_sortable_list = ('username', 'admin', 'email', 'location','aboutme',)
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)
    form_edit_rules = ('username', 'admin', 'email', 'location', 'aboutme',)
    form_create_rules=('username', 'email', 'admin', 'location', 'aboutme')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin



admin.add_view(PostView(Post, db.session, category='Post'))

admin.add_view(UserAdminView(User, db.session))

admin.add_view(CommentView(Comment, db.session))

admin.add_view(FilesView(File, db.session))