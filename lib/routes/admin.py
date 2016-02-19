import csv
import StringIO

from flask import (
    request, render_template, redirect, url_for, flash,
    make_response,
)
from pymongo.errors import DuplicateKeyError

from lib.log import get_logger
from lib.models.game import Game
from lib.models.team import Team
from lib.routes.auth import admin_only
from lib.server import app, form_error
from lib.forms import RegisterForm


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
                team.teamname.encode('utf-8'),
                team.snake_url.encode('utf-8') if team.snake_url else '',
                team.game_mode,
                team.type,
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
    form = RegisterForm()

    if not form.validate_on_submit():
        return render_template('admin/register.html', form=form)

    teamname = form.teamname.data
    password = form.password.data
    email = form.email.data
    game_mode = form.game_mode.data

    existing_team = Team.find_one({'teamname': teamname})
    if existing_team:
        return form_error('Snake name already exists')

    team = Team(
        teamname=teamname,
        password=password,
        member_emails=[email],
        game_mode=game_mode
    )

    try:
        team.insert()
    except DuplicateKeyError:
        return form_error('Got DuplicateKeyError')

    logger.slack('New Registered Team: %s' % team.teamname)

    flash('New Registered Team: %s' % team.teamname)
    return redirect(url_for('register'))
