from myapp.factory import admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.form import rules
from wtforms import widgets,TextAreaField, PasswordField
from myapp.models import User, File, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required


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

