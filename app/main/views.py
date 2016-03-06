from flask import (render_template, flash, redirect, session, url_for, request,
                   Response)
from flask.ext.login import current_user, login_required

from . import main
from .. import db
from ..models import Link, User
from .crawler import crawler
from .forms import EditProfileForm


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
    links = user.links.order_by(Link.date.desc()).filter_by(seen=False).all()
    return render_template('user.html', user=user, links=links)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.username.data = current_user.username
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    return render_template('edit_profile.html', form=form)


@main.route('/crawl/<username>')
def crawl(username):
    user = User.query.filter_by(username=username).first_or_404()
    for result in crawler():
        name, url, image, date = result
        link = Link(name=name, url=url, image=image, date=date, user_id=user.id, seen=False)
        db.session.add(link)
        db.session.commit()
    return Response(status=200, mimetype="application/json")