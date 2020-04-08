from flask import (render_template, request, Blueprint, redirect, url_for, current_app, flash)
from myapp.models import Post, File, Genre, User, Tag
from myapp.files.forms import SearchForm
from myapp.factory import db
from itertools import groupby
from operator import attrgetter
import json

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

@main.route("/relation/user/<int:id>")
def relation1(id):
    user=User.query.get_or_404(id)
    posts=Post.query.filter_by(author=user).all()
    
    return render_template('user_lists.html', posts=posts, user=user)

@main.route("/relation/post/<int:id>")
def relation2(id):
    post=Post.query.get_or_404(id)
    user=User.query.get_or_404(post.author.id)
    posts=Post.query.filter_by(author=user).first()
    rposts=Post.query.filter(Post.id != post.id ).filter_by(category=post.category).limit(5).all()
    return render_template('posts_related.html', rposts=rposts, post=post, user=user)

@main.route("/relation/post/<int:id>")
def relation3(id):   
    try:
        genre=Genre.query.filter_by(title=category).first()
        posts=Post.query.filter_by(category=genre.title).all()
    except:
        return redirect(url_for('main.home'))    
    else:
        return render_template('family_tree.html')    

@main.route("/relations")
def fi():
    return render_template('network.html')

@main.route("/relations/represent")
def relations():
    fonction=lambda x: x
    liste=[]#
    posts=[Post.query.all()]
    posts1=posts
    n=len(posts) #
   
    posts=posts[0]
    posts.sort(key=attrgetter('author.username'))
    posts=groupby(posts, key=attrgetter('author.username'))
       
    for x, y in posts:
        liste1=[(x, i.title) for i in y]
        liste1=[list(x) for x in liste1]
        liste+=liste1#
      
           
    with open('myjson1.txt', 'w') as file:
            
        file.write(str(liste))
    with open('myjson.json', 'a') as file:
        json.dump(liste, file)        
    
    posts=posts1[0]
    posts.sort(key=attrgetter('category'))
    posts=groupby(posts, key=attrgetter('category'))
    
    for x, y in posts:
        liste1=[(x, i.title) for i in y]
        liste1=[list(x) for x in liste1]
        liste+=liste1#
    with open('myjson1.txt', 'a') as file:
            
        file.write(str(liste))
    with open('myjson.json', 'a') as file:
        json.dump(liste, file)  
        

    return render_template('demo.html')        