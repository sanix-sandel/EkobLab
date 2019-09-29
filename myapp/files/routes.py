from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, request, send_file)
from flask_login import current_user, login_required
from myapp import db
from myapp.models import File
from myapp.files.forms import FileForm
import bleach
from io import BytesIO
from flask import Markup



files=Blueprint('files', __name__)

@files.route("/files", methods=['GET', 'POST'])
def allfiles():
    page = request.args.get('page', 1, type=int)
    files = File.query.order_by(File.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('files.html', files=files)

@files.route('/upload', methods=['GET', 'POST'])
def upload():
    form=FileForm()
    if request.method=='POST':
        file=request.files['file']
    
    if form.is_submitted():
        flash('Your file has been uploaded !', 'succes')
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
     
    