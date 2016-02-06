import StringIO, csv

from flask import (
    request, render_template, redirect, url_for, flash,
    make_response,
)
from pymongo.errors import DuplicateKeyError

from lib.log import get_logger
from lib.models.team import Team
from lib.routes.auth import admin_only
from lib.server import app, form_error




logger = get_logger(__name__)


@app.route('/admin/teams')
@admin_only
def list_teams():
    teams = Team.find({})
    teams.sort(key=lambda x: x.teamname)

    fmt = request.args.get('format', 'default')

    if fmt == 'csv':
        si = StringIO.StringIO()
        cw = csv.writer(si)

        for team in teams:
            cw.writerow([
                team.id,
                team.teamname,
                team.type,
                team.game_mode,
                team.is_public
            ])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=teams.csv"
        output.headers["Content-type"] = "text/csv"
        return output

    return render_template('admin/teams.html', teams=teams)

@app.route('/admin/register', methods=['GET', 'POST'])
@admin_only
def register():
    if request.method == 'GET':
        return render_template('admin/register.html')

    data = request.form

    try:
        teamname = data['teamname']
        password = data['password']
        email = data['email']
    except KeyError as e:
        return form_error('Missing field: "%s"' % e.message)

    if not teamname:
        return form_error('Missing team name')

    if len(password) < 6:
        return form_error('Password must be at least 6 characters')

    if not email:
        return form_error('Missing email address')

    existing_team = Team.find_one({'teamname': teamname})
    if existing_team:
        return form_error('Team name already exists')

    team = Team(
        teamname=teamname,
        password=password,
        member_emails=[email]
    )

    try:
        team.insert()
    except DuplicateKeyError:
        return form_error('Team name already exists')

    logger.slack('New Registered Team: %s' % team.teamname)

    flash('New Registered Team: %s' % team.teamname)
    return redirect(url_for('register'))
