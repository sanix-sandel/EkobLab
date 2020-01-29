from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from myapp.factory import db
from myapp.models import Post, Comment, Tag, Reply, Genre, Notif
from myapp.posts.forms import PostForm, TagForm
from myapp.comments.forms import CommentForm
import bleach
from flask import Markup
from flask import send_from_directory
from myapp.files.forms import SearchForm

posts=Blueprint('posts', __name__)


@posts.route("/post/newpost", methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.is_publisher():
        flash('If you want to make post, fisrtly contact the EkoB team. thank you', 'success')
        return redirect(url_for('main.home'))
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        title=title.capitalize()
        genre=form.genre.data
        
        flash('Your Post need a content!', 'succes')
        return redirect(url_for('posts.Newpost', title=title, category=genre.title))   
    return render_template('create_post.html', form=form, title='New Post', legend='New post')


@posts.route("/post/newpost/<string:title>/<string:category>", methods=['GET', 'POST'])
@login_required
def Newpost(title, category):
    tags=Tag.query.all()
    
    if request.method=='POST':
        content=request.form.get('postcontent')
        if content=="":
            flash('The post must have a content', 'danger')
            return redirect(url_for('main.home'))
        else:    
            post=Post(title=title.capitalize(), content=content, author=current_user, category=category)
              
            db.session.add(post)
            db.session.commit()
           
            flash('Your post has been created and saved ! But you have to select some tags please', 'succes')    
            return redirect(url_for('posts.tagin', post_id=post.id))
    return render_template('new_post.html', title='New Post', tags=tags)


@posts.route("/post/newpost/<int:post_id>/tagsinput", methods=['GET', 'POST'])
@login_required
def tagin(post_id):
    form=TagForm()
    tags=Tag.query.all()
    post=Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        flash('Thank you very much '+current_user.username+' !', 'success')
        titles=form.title.data
        return redirect(url_for('posts.tagpicked', post_id=post.id, titles=titles))
    return render_template('tagsinput.html', form=form, tags=tags, post=post)


@posts.route("/post/newpost/<int:post_id>/tagsinput/<string:titles>", methods=['GET', 'POST'])
@login_required
def tagpicked(post_id, titles):
    post=Post.query.get_or_404(post_id)
    titles=titles.split()
    for title in titles:
        title=title.capitalize()
        if Tag.query.filter_by(title=title).count()==1:
            tag=Tag.query.filter_by(title=title).first()
            post.tags.append(tag)
            db.session.commit()
    return redirect(url_for('main.home'))


@posts.route("/post/newpost/<int:post_id>/tagsinput/<int:tag_id>", methods=['GET', 'POST'])
@login_required
def tagpick(post_id, tag_id):
    post=Post.query.get_or_404(post_id)
    tag=Tag.query.get_or_404(tag_id)
    post.tags.append(tag)
    db.session.commit()
    return redirect(url_for('posts.tagin', post_id=post.id))


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.read+=1
    db.session.commit()
    comments= Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.date_posted.desc())\
        .all()
    rposts=Post.query.filter(Post.id != post.id ).filter_by(category=post.category).limit(5).all()
    if request.method=="POST":
        content=request.form.get('comment')
        
        if len(content) > 0:
            return commenter(content, post.id) 

    return render_template('post.html', title=post.title, post=post, rposts=rposts, comments=comments)
                                                  

@posts.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def commenter(content, post_id):
    post=Post.query.get_or_404(post_id)
    author=post.author
    comment=Comment(content=content, author=current_user, post_id=post_id )
    db.session.add(comment)
    db.session.commit()
    post.nbrcomments+=1
    if not current_user==author:
        notif=Notif.query.filter_by(title='PostCommented').first()
        author.notifs.append(notif)
        author.getnot+=1
        db.session.commit()
    flash('Your comment has been added', 'success')
    return redirect (url_for('posts.post', post_id=post.id))
   

@posts.route("/post/<int:post_id>/<int:comment_id>/reply", methods=['GET', 'POST'])
@login_required
def reply(comment_id, post_id):
    comment=Comment.query.get_or_404(comment_id)
    post=Post.query.get_or_404(post_id)
    
    content=request.form.get('reply')
    if len(content)>0:
        reply=Reply(content=content, author=current_user, comment_id=comment.id)
        db.session.add(reply)
        db.session.commit()
        comment.rep=1
        flash('Your reply has been added', 'success')
        return redirect (url_for('posts.post', post_id=post.id))
    else:    
        flash('The reply has no content ', 'danger')
    return redirect (url_for('main.home'))


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
    if request.method=='POST':
   
        content=request.form.get('postcontent')
        if len(content)<0:
            flash('A post must have at least 300 words', 'danger')
            return redirect(url_for('main.home'))

    
        post.content=content
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Post not updated', 'danger')

           
    return render_template('postupdate.html', post=post)



@posts.route("/post/<int:post_id>/updated", methods=['GET', 'POST'])
@login_required
def updatedpost(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method=='POST':
   
        content=request.form.get('postcontent')
        if len(content)<0:
            flash('A post must have at least 300 words', 'danger')
            return redirect(url_for('main.home'))

    
        post.content=content
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Post not updated', 'danger')

        return redirect(url_for('main.home'))
   

@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        if current_user.has_liked_post(post):
            current_user.unlike_post(post)
            post.like-=1
            db.session.commit()
        else:
            current_user.like_post(post)
            post.like+=1
            db.session.commit()   
        return redirect(url_for('posts.post', post_id=post.id))         
       

@posts.route('/home/post/<int:tag_id>/')
def tag_posts(tag_id):
    tag=Tag.query.filter_by(id=tag_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts=tag.posts.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('tag_posts.html', posts=posts)


@posts.route('/home/<string:category>')
def posts_bygenre(category):
    form=SearchForm()
    page = request.args.get('page', 1, type=int)
    genre=Genre.query.filter_by(title=category).first()
    posts=Post.query.filter_by(category=genre.title)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    genres=Genre.query.all()
    return render_template('posts_bygenre.html', genre=genre, posts=posts, genres=genres, form=form)    

        