from flask import render_template

from lib.models.team import Team
from lib.server import app


@app.route('/admin/teams')
def teams():
    teams = Team.find({})
    teams.sort(key=lambda x: x.teamname)

    return render_template('admin/teams.html', teams=teams)
