import os

from config import basedir
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)

from .auth import auth as auth_blueprint
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
