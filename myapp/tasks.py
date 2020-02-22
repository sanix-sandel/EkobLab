from myapp import celery
from myapp.factory import db, mail
from flask import redirect, url_for, current_app, flash
from flask_mail import Message



@celery.task(name="sending_email")
def send_email(msg_dict):  
    msg=Message()
    msg.__dict__.update(msg_dict)
    mail.send(msg)


