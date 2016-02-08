from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField
from wtforms import validators


class LoginForm(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=8)])


class RegisterForm(Form):
    teamname = StringField('Team Name', validators=[validators.InputRequired()])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=8)])
    game_mode = RadioField('Game Mode', choices=[
        ('classic', 'Classic'),
        ('advanced', 'Advanced')
    ])
