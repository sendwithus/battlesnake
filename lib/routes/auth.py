from flask import request, g

from flask.ext.login import (
    LoginManager,
    login_required, login_user, logout_user, current_user
)

from lib.server import _json_response, app
from lib.models.team import Team

import settings.secrets

app.secret_key = settings.secrets.SESSION_KEY

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def load_users():
    g.team = current_user

@app.route('/api/signin', methods=['POST'])
def signin():
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
def signout():
    logout_user()
    return _json_response(msg='Successfully signed out')

@login_manager.user_loader
def load_team(teamname):
    """Given teamname, return the associated Team object.

    :param teamname: team to retrieve
    """
    return Team.find_one({'teamname': teamname})
