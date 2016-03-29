from flask import (render_template, flash, redirect, session, url_for, request,
                   jsonify, current_app, g)
from flask.ext.login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from . import main
from .. import db
from ..models import Link, User
from ..tasks import send_email
from .crawler import crawler
from .forms import EditProfileForm


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.links.order_by(Link.date.desc()).filter_by(seen=False).paginate(
        page, per_page=current_app.config['LINKS_PER_PAGE'],
        error_out=False)
    links = pagination.items
    return render_template('user.html', user=user, links=links,
                           pagination=pagination)
    return render_template('user.html', user=user)

@main.route('/userdata/<username>')
@login_required
def user_data(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.links.order_by(Link.date.desc()).filter_by(seen=False).paginate(
        page, per_page=current_app.config['LINKS_PER_PAGE'],
        error_out=False)
    links = []
    for item in pagination.items:
        links.append({'id': item.id, 'name': item.name, 'url': item.url, 'date': item.date.isoformat()})
    if user == current_user:
        return jsonify({'links':links, 'is_user':True})
    return jsonify({'links':links, 'is_user':False})


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
    results = []
    user = User.query.filter_by(username=username).first_or_404()
    for result in crawler():
        name, url, image, date = result
        link = Link(name=name, url=url, image=image, date=date, user_id=user.id, seen=False)
        try:
            db.session.add(link)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        else:
            results.append({'name': name, 'url': url, 'image': image,
                            'date': date.isoformat()})
    if results:
        send_email(user.email, 'You got some new episodes', 'email/episodes',
                   user=user, results=results)
    return jsonify({'results': results})


@main.route('/delete-links', methods=['POST'])
@login_required
def delete_links():
    link_ids = request.form['selected'].split(',')
    print(link_ids)
    if link_ids is None:
        flash('Links not found.')
        return redirect(url_for('main.user', username=current_user.username))
    links = Link.query.filter(Link.id.in_(link_ids)) #.delete()
    for link in links:
        db.session.delete(link)
    db.session.commit()
    flash('Your links have been deleted.')
    return redirect(url_for('main.user', username=current_user.username))


@main.route('/set-seen', methods=['POST'])
@login_required
def set_seen():
    link_ids = request.form['selected'].split(',')
    if not link_ids:
        flash('Links not found.')
        return redirect(url_for('main.user', username=current_user.username))
    links = Link.query.filter(Link.id.in_(link_ids))
    for link in links:
        link.seen = True
        db.session.add(link)
    db.session.commit()
    flash('Your links have been set to  seen.')
    return redirect(url_for('main.user', username=current_user.username))