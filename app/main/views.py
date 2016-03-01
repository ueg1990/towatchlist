from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required

from . import main
from ..models import User


@main.route('/')
@main.route('/index')
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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)