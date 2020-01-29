from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from myapp.factory import db
from myapp.models import Comment, Post
from myapp.comments.forms import CommentForm
  


comments=Blueprint('comments', __name__)

"""
@login_required
@comments.route("/post/<int:post_id>/comment", methods=["POST", "GET"])
def get_comment(post_id):
    
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter_by(id=post_id)
    post=post.one()
   
    comments= Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.date_posted.desc())\
        .paginate(page=page, per_page=5)

    if form.validate_on_submit():
        reply=Comment(content=form.content.data, author=current_user, post_id=post_id, 
        receveur=comment.author.username)
        flash('your Reply has been successfully added', 'success')
        db.session.add(reply) 
        db.session.commit()
           
        return redirect(url_for('comments.get_comment()', post_id=post.id))
      
    return render_template('postcomments.html', form=form, post=post, comments=comments)
"""