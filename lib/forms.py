from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class LoginForm(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = StringField('Password', validators=[validators.DataRequired(), validators.Length(min=8)])
