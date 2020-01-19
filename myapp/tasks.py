from myapp import celery, db, mail
from flask import redirect, url_for, current_app
from flask_mail import Message
from myapp import create_app

@celery.task(name="sending_email")
def send_email(msg_dict):
    Myapp=create_app()
    with Myapp.app_context():
        msg=Message()
        msg.__dict__.update(msg_dict)
        mail.send(msg)