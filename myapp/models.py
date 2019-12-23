from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from myapp import (db, login_manager, admin, bcrypt)
from flask import (current_app, flash, redirect,  url_for)
from flask_login import UserMixin, current_user, login_required
from myapp import admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_admin.form import rules
from wtforms import widgets,TextAreaField, PasswordField



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


notifs=db.Table('user_notifs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('notif_id', db.Integer, db.ForeignKey('notif.id'))

)

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    location=db.Column(db.String(30), nullable=True)  #ici
    member_since=db.Column(db.DateTime(), default=datetime.utcnow)
    notifs=db.relationship('Notif', secondary=notifs, backref=db.backref('user', lazy='dynamic'), lazy='dynamic')
    comment=db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    reply=db.relationship('Reply', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    files=db.relationship('File', backref='uploader',lazy='dynamic', cascade='all, delete-orphan')
    aboutme=db.Column(db.Text, nullable=True)
    admin=db.Column(db.Boolean(), default=False)
    publisher=db.Column(db.Boolean(), default=False)
    confirmed=db.Column(db.Boolean(), default=False)
    liked=db.relationship('PostLike', backref='liker', lazy='dynamic', cascade='all, delete-orphan')
    recommendations=db.relationship('Ebook', backref='recommender', lazy='dynamic', cascade='all, delete-orphan')
   
    
    extend_existing=True

    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.admin         

    def is_publisher(self):
        return self.publisher    

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    def generate_confirmation_token(self, expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

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


tags=db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))

)


class Post(db.Model):
   
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), nullable=False)   
    date_posted=db.Column(db.DateTime(), nullable=False, index=True, default=datetime.utcnow)
    content=db.Column(db.UnicodeText, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    genre=db.Column(db.String(20), nullable=False, default='chat')
    comment=db.relationship('Comment', backref='post_comments', lazy='dynamic', cascade='all, delete-orphan')
    tags=db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')
    reads=db.Column(db.Integer, default=0)
    
    nbcomments=db.Column(db.Integer, default=0)
    liked=db.relationship('PostLike', backref='post_liked', lazy='dynamic', cascade='all, delete-orphan')
    nbrlikes=db.Column(db.Integer, default=0)

   
    extend_existing=True

    @property
    def read(self):
        return self.reads

    @read.setter
    def read(self, r):
        self.reads=r
        

    @property
    def like(self):
        return self.nbrlikes

    @like.setter
    def like(self, r):
        self.nbrlikes=r        

    @like.setter
    def dislike(self):
        self.nbrlikes-=1     

    @property
    def nbrcomments(self):
        self.nbcomments+=1

    @nbrcomments.setter
    def nbrcomments(self, c):
        self.nbcomments=c
       
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)  
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply=db.relationship('Reply', backref='comment', lazy='dynamic', cascade='all, delete-orphan')
    nbrep=db.Column(db.Integer, default=0)

    @property
    def rep(self):
        return self.rep

    @rep.setter
    def rep(self, rep):
        self.nbrep+=rep    

class Reply(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_id=db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    
    def __repr__(self):
        return f"Reply('{self.author.username}')"
    

class File(db.Model):
    __searchable__= ['title']
   

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(40), nullable=False)   
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data=db.Column(db.LargeBinary, nullable=False) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    cover=db.relationship('Cover', backref='file', lazy='dynamic', cascade='all, delete-orphan')
    downloaded=db.Column(db.Integer, default=0)
    _img_id=db.Column(db.Integer, default=0)
    img_id=_img_id

    extend_existing=True


    def _set_img(self, id):
        self._img_id=id

    def downloads(self):
        self.downloaded+=1
    

    def __repr__(self):
        return f"File('{self.title}', '{self.date_posted}')"    

    _img_id=property(_set_img)


class Cover(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data=db.Column(db.LargeBinary, nullable=False)
    file_id=db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

    extend_existing=True

class PostLike(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Ebook(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title=db.Column(db.String(40), nullable=False)
    author=db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"Ebook('{self.title}', '{self.date_posted}')"    


class Tag(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(20))

    def __repr__(self):
        return f"Tag('{self.title}')" 

class Notif(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(20))
    message=db.Column(db.Text())



    def __repr__(self):
        return f"Notif(' : {self.message}')" 

              

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget=CKTextAreaWidget()        

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.admin):
            return redirect(url_for('users.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user is not None and user.verify_password(form.password.data):
                login.login_user(user)
            else:
                flash('Invalid username or password.')
        if login.current_user.is_authenticated:
            return redirect(url_for('main.home'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout')
    @login_required
    def logout(self):
        login.logout_user()
        return redirect(url_for('users.login'))


class PostView(ModelView):
    form_overrides=dict(content=CKTextAreaField)
    column_searchable_list=('title', 'content')
    column_exclude_list=('content')
   
    create_template='new.html'
    edit_template='new.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class CommentView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class ReplyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin    


class CoverView(ModelView):
    column_exclude_list=('data')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin



class FilesView(ModelView):
    column_exclude_list = ('data',)
    column_searchable_list=('title',)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin   


class EbookView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin 

class TagView(ModelView):
    column_searchable_list=('title',)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin  

class NotifView(ModelView):
    column_searchable_list=('message',)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin                               

class UserAdminView(ModelView):
    column_searchable_list=('username',)
    column_sortable_list = ('username', 'admin', 'email', 'location','aboutme', 'confirmed',)
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)
    form_edit_rules = ('username', 'admin', 'email', 'location', 'aboutme', 'publisher', 'confirmed')
    form_create_rules=('username', 'email', 'admin', 'location', 'aboutme')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(PostView(Post, db.session, category='Post'))

admin.add_view(UserAdminView(User, db.session))

admin.add_view(CommentView(Comment, db.session))

admin.add_view(ReplyView(Reply, db.session))

admin.add_view(FilesView(File, db.session))

admin.add_view(EbookView(Ebook, db.session))

admin.add_view(CoverView(Cover, db.session))

admin.add_view(TagView(Tag, db.session))

admin.add_view(NotifView(Notif, db.session))
