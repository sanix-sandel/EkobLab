from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
import bleach


class PostForm(FlaskForm):
    title=StringField('Title/Titre', validators=[DataRequired(), Length(min=5, max=50)])
    content=TextAreaField("What's up ?", validators=[DataRequired()])
    submit=SubmitField('Post/poster')
    

