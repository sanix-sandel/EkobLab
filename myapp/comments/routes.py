from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from myapp import db
from myapp.models import Comment, Post
from myapp.comments.forms import CommentForm, ReplyForm
  


comments=Blueprint('comments', __name__)


@login_required
@comments.route("/post/<int:post_id>/comment", methods=["POST", "GET"])
def get_comment(post_id):
    form=ReplyForm()
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter_by(id=post_id)
    post=post.one()
    comments= Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.date_posted.desc())\
        .paginate(page=page, per_page=5)
      
    return render_template('postcomments.html', form=form, post=post, comments=comments)

