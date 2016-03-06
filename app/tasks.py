from threading import Thread

from flask import render_template
from flask.ext.mail import Message

from . import app, mail

PREFIX = '[ToWatchList] '
MAIL_SENDER = 'ToWatchList Admin <{0}>'.format(app.config['MAIL_USERNAME'])


def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	msg = Message(PREFIX + subject, sender=MAIL_SENDER, recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr