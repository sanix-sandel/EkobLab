from flask import render_template, request, Blueprint
from myapp.models import Post

main=Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/admin')
def securityblock():
    return render_template('errors/404.html'), 404


@main.route("/trends")
def trend():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.reads.desc()).paginate(page=page, per_page=5)
    return render_template('trending.html', posts=posts)
