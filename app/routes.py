from random import randint

from app import my_app, db, mail
from flask import render_template, request, redirect, url_for, flash
from app.models import User, Post
from datetime import datetime
from flask_login import login_required, current_user, login_user, logout_user
from flask_mail import Message
from hashlib import md5

@my_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@my_app.route('/')
@my_app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if 'page' in request.args:
            page = int(request.args['page'])
        else:
            page=1
        all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,10,False)
        return render_template("index.html", posts=all_posts)
    elif request.method == "POST":
        text = request.form.get("text").strip()
        if text =='':
            flash('Empty message')
            return redirect(url_for('index'))
        post = Post(text=text, author=current_user, timestamp=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@my_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        form = request.form
        username = form.get('username')
        remember = bool(form.get('remember'))
        password = form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        else:
            flash("Invalid name or password")
            return redirect(url_for('login'))


@my_app.route('/regist', methods=['GET', 'POST'])
def regist():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("regist.html")
    if request.method == "POST":
        form = request.form
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
        u = User(username=username, email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))


@my_app.route('/profile/<user_name>')
def profile(user_name):
    user = User.query.filter_by(username=user_name).first_or_404()
    return render_template("profile.html", user=user)


@my_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@my_app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template("reset_password.html")
    if request.method == "POST":
        form = request.form
        email = form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:

            new_password=generate_password()
            user.set_password(new_password)
            db.session.commit()
            send_email(email,new_password)
        return render_template("reset_password.html")


def send_email(user_email, new_password):
    message=Message("Microblog. Reset password", sender="micro.blog@bk.ru", recipients=[user_email])
    message.body = f"Hello, you request reset password.\nYour new password: {new_password}"
    mail.send(message)

def generate_password():
    return md5 (str(randint(0,100)).encode('utf-8')).hexdigest()[:9]


@my_app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404


@my_app.errorhandler(500)
def error500(error):
    return render_template('500.html'),500