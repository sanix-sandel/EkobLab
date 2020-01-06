from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField 
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from myapp.models import Genre


def choice_query():
    return Genre.query


class PostForm(FlaskForm):
    title=StringField('Title/Titre', validators=[DataRequired(), Length(min=5, max=150)])
    genre=QuerySelectField('Genre', query_factory=choice_query, allow_blank=True, get_label='title')
    submit=SubmitField('Continuer')
    
class TagForm(FlaskForm):
    title=StringField('', validators=[DataRequired(), Length(min=2, max=80)]) 
    submit=SubmitField('validate')   

