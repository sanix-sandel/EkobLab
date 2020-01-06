from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from myapp import db, bcrypt
from myapp.models import User, Post
from myapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from myapp.users.utils import save_picture, send_reset_email, send_email
from myapp import mail


users=Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('main.home')) #si le user est authentifié il est renvoyé à la page d'acceuil
    form=RegistrationForm()
    if form.validate_on_submit():#si il valide son enregistrement, ses donnnées sont envoyées à la DB
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password, admin=True, publisher=True )
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,'Confirm your Account', 'registration_confirmation', user=user, token=token)
        flash('A confirmation mail has been sent to you ! Check your mail box and confirm your account please !', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.confirmed:
                flash(''+user.username +' You have to confirm your mail account please, check your mail box, and click on the link provided. thank you', 'danger')
                return redirect(url_for('users.login'))
             #alors on active le remember me, et ensuite on le renvoie a la prochaine page get by request
            flash('Welocome back '+user.username+'', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))#si il voulait se connecter à 
           
            #une page on le renvoie a la page, sinon à a page d'acceuil
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

    
@users.route("/account", methods=['GET', 'POST'])
@login_required #il doit etre connecté
def account():
    form = UpdateAccountForm() 
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location=form.location.data      #Ici
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data=current_user.location #ici
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


    
@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    page=request.args.get('page', 1, type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)    



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
  

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)        




@users.route("/confirm/<int:id>/<token>")
def confirm(id, token):
    user=User.query.get_or_404(id)
    if user.confirmed:
        return redirect(url_for('main.home'))
    if user.confirm(token):
        
        db.session.commit()
        flash('You have confirmed your account, thank you !')
         
    else:
        flash('The confirmation link is invalid or has expired')
      
    return redirect(url_for('main.home'))              