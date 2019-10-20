from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
import bleach
from flask_wtf.file import FileField, FileAllowed



class FileForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    description=TextAreaField('About the doc')
    filedata = FileField('Update the doc', validators=[FileAllowed(['pdf'])])
    submit=SubmitField('Upload')
    

class FileCommand(FlaskForm):
    title=StringField('Title / Titre', validators=[DataRequired()])  
    author=StringField('Author / Auteur', validators=[DataRequired()])
    submit=SubmitField('Command')  