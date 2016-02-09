from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField, SelectField
from wtforms import validators


class LoginForm(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=6)])


class RegisterForm(Form):
    teamname = StringField('Team Name', validators=[validators.InputRequired()])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=6)])
    game_mode = RadioField('Game Mode', choices=[
        ('classic', 'Classic ($300 Grand Prize)'),
        ('advanced', 'Advanced ($1,000 Grand Prize)')
    ], default='classic')


class TeamUpdateForm(Form):
    teamname = StringField('Team Name', validators=[validators.InputRequired()])
    snake_url = StringField('Snake URL', validators=[validators.Optional()])
    password = PasswordField('Change Password', validators=[validators.Optional(), validators.Length(min=6)])
    add_member = StringField('Add Team Member', validators=[validators.Optional(), validators.Email()])
    type = SelectField('Team Type', choices=[
        ('normal', 'Normal'),
        ('bounty', 'Bounty'),
        ('test', 'Test'),
        ('admin', 'Admin'),
    ], default='normal')
    game_mode = SelectField('Game Mode', choices=[
        ('classic', 'Classic ($300 Grand Prize)'),
        ('advanced', 'Advanced ($1,000 Grand Prize)')
    ], default='classic')
    is_public = BooleanField('Make snake public?', default=False)
