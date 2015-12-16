from flask import g
from flask.ext.login import login_required

from lib.server import _json_response, app

@app.route('/api/team')
@login_required
def team_info():
    return _json_response(data={
        'teamname': g.team.teamname
    })
