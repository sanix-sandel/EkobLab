from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from myapp import db
from myapp.models import Post, Comment
from myapp.posts.forms import PostForm
from myapp.comments.forms import CommentForm
import bleach
from flask import Markup

posts=Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=(form.content.data), author=current_user, reads=0, nbcomments=0)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'succes')
        return redirect(url_for('main.home'))   
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')



@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.reads+=1
    db.session.commit()
    form=CommentForm()
   
    rposts=Post.query.filter_by(genre=post.genre).filter(id != post.id).limit(5).all()
    if form.is_submitted():
        comment=Comment(content=form.content.data, author=current_user, post_id=post_id )
        db.session.add(comment)
        post.nbrcomments()
        db.session.commit()
        flash('Your comment has been added', 'success')
        return redirect (url_for('posts.post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, form=form, rposts=rposts)
                          
                           


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))                           


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


