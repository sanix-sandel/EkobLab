from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, request, send_file, Response, g, current_app)
from flask_login import current_user, login_required
from myapp import db
from myapp.models import File, Ebook, Cover, User, Notif, Genre
from myapp.files.forms import FileForm, EbookForm, SearchForm
import bleach
from io import BytesIO
from flask import Markup
from flask_mail import Message
from myapp import mail
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
    if request.method=='POST':

        if 'file' not in request.files:
            flash('No file part !')
        file=request.files['file']

        if file.filename=='':
            flash('No file selected ', 'danger')
            return redirect(request.url)    
        if not allowed_file(file.filename):
            flash('Only PDF files, please', 'danger')

        cover=request.files['cover']
        if not file_allowed(cover.filename):
            flash('Only png, jpeg, jpg files allowed')
         
    #if form.is_submitted():
        else:
            if form.validate_on_submit():


                flash('Your file has been successfully uploaded !', 'succes')
                
                file.seek(0, os.SEEK_END)
                file_length=file.tell()
                category=form.genre.data
                newFile=File(title=form.title.data.capitalize(), data=file.read(), 
                    description=form.description.data, uploader=current_user, downloaded=0,
                     file_size=(file_length/1000), category=category.title)
                cover=Cover(file=newFile, data=cover.read())
                db.session.add(cover)
                db.session.commit()  
                newFile.img_id=cover.id
                db.session.add(newFile)
                db.session.commit() 
                return redirect(url_for('files.allfiles')) 
              
    return render_template("fileupload.html", form=form)


@login_required
@files.route('/home/upload/<int:recommender_id>', methods=['GET', 'POST'])
def uploadv(recommender_id):
    form=FileForm()
    recommender=User.query.filter_by(id=recommender_id).first()
    if request.method=='POST':

        if 'file' not in request.files:
            flash('No file part !')
        file=request.files['file']

        if file.filename=='':
            flash('No file selected ', 'danger')
            return redirect(request.url)    
        if not allowed_file(file.filename):
            flash('Only PDF files, please', 'danger')

        cover=request.files['cover']
        if not file_allowed(cover.filename):
            flash('Only png, jpeg, jpg files allowed')
         
    #if form.is_submitted():
        else:
            if form.validate_on_submit():
                flash('Your file has been successfully uploaded !', 'succes')
                flash('thank You very much, Keep helping the biblio grow', 'succes')
                file.seek(0, os.SEEK_END)
                file_length=file.tell()
                category=form.genre.data
                newFile=File(title=form.title.data.capitalize(), data=file.read(), 
                    description=form.description.data, uploader=current_user, downloaded=0,
                    file_size=(file_length/1000), category=category.title)
                cover=Cover(file=newFile, data=cover.read())
                db.session.add(cover)
                current_user.getbooks+=1
                db.session.commit()  
                newFile.img_id=cover.id
                db.session.add(newFile)
                db.session.commit() 
            

                msg = Message('E-Books Recommendation',
                    sender='techyintelo@gmail.com',
                    recipients=[recommender.email])
                msg.body = f'''Woopi ! the ebook you needed has been uploaded by a volunteer ! You can check it out 
                If you did not make this request then simply ignore this email and no changes will be made.
                TechyB Team.
                '''
                mail.send(msg)
                notif=Notif.query.filter_by(title='EbookUploaded').first()
                recommender.notifs.append(notif)
                recommender.getnot+=1
                db.session.commit()
                return redirect(url_for('files.allfiles')) 
              
    return render_template("fileupload2.html", form=form)


@login_required
@files.route("/file/<int:file_id>", methods=['GET', 'POST'])
def file(file_id):
    
    file = File.query.get_or_404(file_id)
    return render_template('file.html', title=file.title, file=file, file_id=file_id, cover=file.cover, img_id=file.img_id)

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
        msg = Message('E-Books Recommendation',
                  sender='techyintelo@gmail.com',
                  recipients=[current_user.email])
        msg.body = f'''We received your E-Book recommendation , Soon we'll 
        send you by this mail a link in order to download the E-Book. 
        If you did not make this request then simply ignore this email and no changes will be made.
        TechyB Team.
        '''
        mail.send(msg)
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
        .paginate(page=page, per_page=5)
    return render_template('files_bygenre.html', files=files, genre=genre, form=form, genres=genres)





