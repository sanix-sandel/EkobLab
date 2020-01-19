from flask import (render_template, request, Blueprint, redirect, url_for, current_app, flash)
from myapp.models import Post, File, Genre
from myapp.files.forms import SearchForm
from myapp import db

main=Blueprint('main', __name__)


@main.route("/",methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form=SearchForm()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    genres=Genre.query.all()
    form=SearchForm()
    if form.validate_on_submit():
        searched=form.search.data
        searched=searched.capitalize()
        flash('Search results of the keyword '+searched, 'success')
        
        
        return search_results(searched)
       
    return render_template('home.html', posts=posts, form=form, genres=genres)


@main.route('/home', methods=['GET', 'POST'])
def search_results(searched):  
    """Results=File.query.filter_by(title=searched).all()"""
    Results1=File.query.filter(File.title.like('%'+searched+'%'))
    Results2=Post.query.filter(Post.title.like('%'+searched+'%'))
    total1=Results1.count()
    total2=Results2.count()
    return render_template('search.html', results1=Results1, results2=Results2, total1=total1, total2=total2)
                           

@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/admin')
def securityblock():
    return render_template('errors/404.html'), 404


@main.route("/home/trends")
def trend():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.reads.desc()).paginate(page=page, per_page=5)
    return render_template('trending.html', posts=posts)

