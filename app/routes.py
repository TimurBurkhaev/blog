from app import my_app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, Post
from datetime import datetime
from flask_login import login_required, current_user, login_user, logout_user


@my_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@my_app.route('/')
@my_app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        all_posts = Post.query.all()
        return render_template("index.html", posts=all_posts)
    elif request.method == "POST":
        text = request.form.get("text")
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
        print(1)
