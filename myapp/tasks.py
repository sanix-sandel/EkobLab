from myapp import celery, db, mail, create_app
from flask import redirect, url_for, current_app
from flask_mail import Message



@celery.task(name="sending_email")
def send_email(msg_dict):  
    msg=Message()
    msg.__dict__.update(msg_dict)
    mail.send(msg)