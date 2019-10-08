from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
import bleach


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField("What's up ?", validators=[DataRequired()])
    submit=SubmitField('Post')

