from flask import (
    request, render_template, redirect, url_for, flash,
)
from pymongo.errors import DuplicateKeyError

from lib.log import get_logger
from lib.models.team import Team
from lib.routes.auth import admin_only
from lib.server import app, form_error


logger = get_logger(__name__)


@app.route('/admin/teams')
@admin_only
def teams():
    teams = Team.find({})
    teams.sort(key=lambda x: x.teamname)

    return render_template('admin/teams.html', teams=teams)


@app.route('/admin/register', methods=['GET', 'POST'])
@admin_only
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    data = request.form

    try:
        teamname = data['teamname']
        password = data['password']
    except KeyError as e:
        return form_error('Missing field: "%s"' % e.message)

    if teamname == '':
        return form_error('Missing field: "teamname"')

    if password == '':
        return form_error('Missing field: "password"')

    existing_team = Team.find_one({'teamname': teamname})
    if existing_team:
        return form_error('Team name already exists')

    team = Team(teamname=teamname, password=password)

    try:
        team.insert()
    except DuplicateKeyError:
        return form_error('Team name already exists')

    logger.slack('New Registered Team: %s' % team.teamname)

    flash('New Registered Team: %s' % team.teamname)
    return redirect(url_for('team'))
