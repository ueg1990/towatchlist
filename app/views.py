from app import app, login_manager, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'title': 'Match of the Day', 
            'url': 'http://www.fullmatchesandshows.com/2016/02/13/bbc-match-of-the-day-week-26-full-show/' 
        },
        { 
            'title': 'Europen Football Show', 
            'url': 'http://www.fullmatchesandshows.com/2016/02/21/european-football-show-21st-february-2016/' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))