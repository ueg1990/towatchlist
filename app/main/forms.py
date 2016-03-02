from flask.ext.wtf import Form
from wtforms import (StringField, TextAreaField, BooleanField, SelectField,
                     SubmitField)
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User


class EditProfileForm(Form):
    username = StringField('Username', validators=[Length(0, 120)])
    first_name = StringField('First Name', validators=[Length(0, 120)])
    last_name = StringField('Last Name', validators=[Length(0, 120)])
    submit = SubmitField('Submit')