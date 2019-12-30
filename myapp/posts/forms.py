from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
import bleach


class PostForm(FlaskForm):
    title=StringField('Title/Titre', validators=[DataRequired(), Length(min=5, max=50)])
    submit=SubmitField('Continuer')
    
class TagForm(FlaskForm):
    title=StringField('', validators=[DataRequired(), Length(min=2, max=20)]) 
    submit=SubmitField('validate')   
