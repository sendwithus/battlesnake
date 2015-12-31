from flask import (
    request, g,
    render_template, redirect, url_for, flash,
)
from pymongo.errors import DuplicateKeyError

from flask.ext.login import (
    LoginManager,
    login_required, login_user, logout_user, current_user
)

from lib.server import app, _json_response, _form_error
from lib.models.team import Team

import settings.secrets

app.secret_key = settings.secrets.SESSION_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_request
def load_users():
    g.team = current_user

@app.route('/api/signin', methods=['POST'])
def signin_api():
    teamname = request.json.get('teamname')
    password = request.json.get('password')
    team = load_team(teamname)

    if team and team.check_password(password):
        login_user(team)
        return _json_response(msg='Successfully signed in')
    else:
        return _json_response(msg='Incorrect teamname or password', status=401)

@app.route("/api/signout", methods=['POST'])
@login_required
def signout_api():
    logout_user()
    return _json_response(msg='Successfully signed out')

@login_manager.user_loader
def load_team(teamname):
    """Given teamname, return the associated Team object.

    :param teamname: team to retrieve
    """
    return Team.find_one({'teamname': teamname})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    data = request.form
    next = request.values.get('next') or 'play'

    try:
        teamname = data['teamname']
        password = data['password']
    except KeyError as e:
        return _form_error('Missing field: "%s"' % e.message)

    if teamname == '':
        return _form_error('Missing field: "teamname"')

    if password == '':
        return _form_error('Missing field: "password"')

    existing_team = Team.find_one({'teamname': teamname})
    if existing_team:
        return _form_error('Team name already exists')

    team = Team(teamname=teamname, password=password)

    try:
        team.insert()
    except DuplicateKeyError:
        return _form_error('Team name already exists')

    login_user(team)

    return redirect(next)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    data = request.form
    next = request.values.get('next') or 'play'

    try:
        teamname = data['teamname']
        password = data['password']
    except KeyError as e:
        return _form_error('Missing field: "%s"' % e.message)

    team = load_team(teamname)

    if team and team.check_password(password):
        login_user(team)
        return redirect(next)
    else:
        return _form_error('Bad team name or password')


@app.route("/logout")
@login_required
def logout():
    flash('You have been logged out')
    logout_user()
    return redirect(url_for('login'))


@app.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    team = g.team
    data = request.form

    if request.method == 'GET':
        return render_template('team.html', team=team)

    # TODO: check for duplicate team name and allow updating
    for field in ['snake_url']:
        if field in data:
            setattr(team, field, data[field])

    email = data.get('add_member')
    if email and email not in team.member_emails:
        team.member_emails.append(email)

        team.save()

        flash('Member added to team')
        return redirect(url_for('team'))

    team.save()

    # Log in team again in case team name changed
    login_user(team)

    return redirect(url_for('team'))
