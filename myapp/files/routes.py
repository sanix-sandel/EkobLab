from flask import (render_template, url_for, flash, make_response,
                   redirect, request, abort, Blueprint, request, send_file, Response, g, current_app)
from flask_login import current_user, login_required
from myapp.factory import db, mail
from myapp.models import File, Ebook, Cover, User, Notif, Genre
from myapp.files.forms import FileForm, EbookForm, SearchForm
from myapp.users.utils import save_picture, send_reset_email, send_mail, msg_to_dict
import bleach
from io import BytesIO
from flask import Markup
from flask_mail import Message
from sqlalchemy.orm.util import join
from datetime import datetime
import os



files=Blueprint('files', __name__)


ALLOWED_EXTENSIONS=set(['pdf', 'epub'])
EXTENSIONS_ALLOWED=set(['jpeg', 'png', 'jpg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS_ALLOWED


@login_required
@files.route("/files", methods=['GET', 'POST'])
def allfiles():
    page = request.args.get('page', 1, type=int)
    files = File.query.order_by(File.date_posted.desc()).paginate(page=page, per_page=12)
    genres=Genre.query.all()
    return render_template('files.html', files=files, genres=genres)


@files.route('/img/<int:img_id>', methods=['GET', 'POST'])
def serve_image(img_id):
    image=Cover.query.get_or_404(img_id)
    return image.data



@login_required
@files.route('/home/upload', methods=['GET', 'POST'])
def upload():
    form=FileForm()      
    #if form.is_submitted():
        
    if form.validate_on_submit():
        flash('Your file has been successfully uploaded !', 'succes')        
        form.filedata.data.seek(0, os.SEEK_END)
        file_length=form.filedata.data.tell()/1000000
        file_length=str(file_length)[:4]
        category=form.genre.data
        newFile=File(title=form.title.data.title(), data=form.filedata.data.read(), 
            description=form.description.data, uploader=current_user, downloaded=0,
            file_size=file_length, category=category.title, auteur=form.auteur.data)
        cover=Cover(file=newFile, data=form.cover.data.read())
        flash('Your file has been successfully uploaded', 'success')
        db.session.add(cover)            
        db.session.commit()  
        newFile.img_id=cover.id
        db.session.add(newFile)
        db.session.commit()
              
    return render_template("fileupload.html", form=form)



@login_required
@files.route('/home/upload/<int:recommender_id>/<int:ebook_id>', methods=['GET', 'POST'])
def uploadv(recommender_id, ebook_id):
    form=FileForm()
    recommender=User.query.filter_by(id=recommender_id).first()
    ebook=Ebook.query.filter_by(id=ebook_id).first()
    flash('Keep making the library grow for the sake of all', 'success')
    if form.validate_on_submit():
               
        form.filedata.data.seek(0, os.SEEK_END)
        file_length=form.filedata.data.tell()/1000000
        file_length=str(file_length)[:4]
        category=form.genre.data
        newFile=File(title=ebook.title.title(), data=form.filedata.data.read(), 
            description=form.description.data, uploader=current_user, downloaded=0,
            file_size=file_length, category=category.title, auteur=form.auteur.data)
        cover=Cover(file=newFile, data=form.cover.data.read())
        flash('Your file has been successfully uploaded. Thank you very much !', 'success')
        db.session.add(cover)            
        db.session.commit()  
        newFile.img_id=cover.id
        db.session.add(newFile)
        db.session.commit()
    
        send_mail(recommender.email,'Recommended Ebook uploaded', 'ebookuploaded', username=recommender.username, title=newFile.title)
        return redirect(url_for('files.allfiles')) 
              
    return render_template("fileupload2.html", form=form, title=ebook.title.capitalize())


@login_required
@files.route("/file/<int:file_id>", methods=['GET', 'POST'])
def file(file_id):
    
    file = File.query.get_or_404(file_id)
    return render_template('file.html', title=file.title, file=file, file_id=file_id, cover=file.cover, file_size=file.file_size, img_id=file.img_id)

@login_required
@files.route('/file/<int:file_id>/download', methods=['POST', 'GET'])
def download(file_id):
    file_data=File.query.get_or_404(file_id)
    file_data.downloads()
    db.session.commit()
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.title, as_attachment=True) 



@login_required
@files.route("/home/recommend", methods=['GET', 'POST'])
def recommend():
    form=EbookForm()
    if form.validate_on_submit():
        flash("Your recommendation is received, we'll reply soon", 'success')
        ebook=Ebook(title=form.title.data.capitalize(), author=form.author.data, recommender=current_user)
        db.session.add(ebook)
        db.session.commit()
        send_mail(current_user.email,'Recommendation of an Ebook', 'ebookrecommendation', username=current_user.username, title=ebook.title)
        return redirect(url_for('main.home'))  
    return render_template('recommend.html', form=form)


@login_required
@files.route('/home/ebooks', methods=['GET'])    
def ebooks():
    page = request.args.get('page', 1, type=int)
    ebooks = Ebook.query.order_by(Ebook.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('Ebooks.html', ebooks=ebooks)


@files.route('/home/files/<string:category>')
def files_bygenre(category):
    form=SearchForm()
    page = request.args.get('page', 1, type=int)
    genre=Genre.query.filter_by(title=category).first()
    genres=Genre.query.all()
    files=File.query.filter_by(category=genre.title)\
        .order_by(File.date_posted.desc())\
        .paginate(page=page, per_page=6)
    return render_template('files_bygenre.html', files=files, genre=genre, form=form, genres=genres)





