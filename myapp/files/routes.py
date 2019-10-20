from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, request, send_file)
from flask_login import current_user, login_required
from myapp import db
from myapp.models import File
from myapp.files.forms import FileForm, FileCommand
import bleach
from io import BytesIO
from flask import Markup
from flask_mail import Message
from myapp import mail



files=Blueprint('files', __name__)


ALLOWED_EXTENSIONS=set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files.route("/files", methods=['GET', 'POST'])
def allfiles():
    page = request.args.get('page', 1, type=int)
    files = File.query.order_by(File.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('files.html', files=files)

@files.route('/upload', methods=['GET', 'POST'])
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
    #if form.is_submitted():
        else:

            flash('Your file has been successfully uploaded !', 'succes')
            newFile=File(title=file.filename, data=file.read(), description=form.description.data, uploader=current_user, downloaded=0)
            db.session.add(newFile)
            db.session.commit()    
    return render_template("fileupload.html", form=form)
    



@login_required
@files.route("/file/<int:file_id>", methods=['GET', 'POST'])
def file(file_id):
    
    file = File.query.get_or_404(file_id)
    return render_template('file.html', title=file.title, file=file, file_id=file_id)

@login_required
@files.route('/file/<int:file_id>/download', methods=['POST', 'GET'])
def download(file_id):
    file_data=File.query.get_or_404(file_id)
    file_data.downloads()
    db.session.commit()
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.title, as_attachment=True) 
     

@login_required
@files.route("/recommand", methods=['GET', 'POST'])
def recommand():
    form=FileCommand()
    if form.is_submitted():
        flash("Your recommandation is received, we'll reply soon", 'success')
        msg = Message('E-Books Recommandation',
                  sender='techyintelo@gmail.com',
                  recipients=[current_user.email])
        msg.body = f'''We received your command , Soon we'll send you by this mail a link i 
        order to download the E-Book 
        If you did not make this request then simply ignore this email and no changes will be made.
        TechyB Team.
        '''
        mail.send(msg)
        return redirect(url_for('main.home'))  
    return render_template('recommand.html', form=form)
    