from flask import (
    request, g, session,
    render_template, redirect, url_for, flash,
    abort
)

from lib.server import form_error, json_response, app
from lib.models.game import Game
from lib.models.team import Team

import lib.ai as ai
import lib.game.engine as engine


@app.route('/team', methods=['GET'])
@app.route('/admin/teams/<team_id>', methods=['GET'])
def get_team(team_id=None):
    """
    Show team profile page

    Can be used by admins to view any team by adding ?admin_override_id=<team_id> to URL
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)

    return render_template('team.html', team=team, is_admin=is_admin)


@app.route('/team', methods=['POST'])
@app.route('/admin/teams/<team_id>', methods=['POST'])
def update_team(team_id=None):
    """
    Update team profile

    Can be used by admins to update any team by adding ?admin_override_id=<team_id> to URL
    """
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team
    data = request.form

    # Admin override
    if team_id:
        team = Team.find_one({'_id': team_id})
        if not is_admin or not team:
            abort(404)

    # Validate teamname
    teamname = data.get('teamname')
    other_team = Team.find_one({'$and': [
        {'teamname': teamname},
        {'_id': {'$ne': team.id}},
    ]})
    if other_team:
        return form_error('Team name already in use')
    team.teamname = teamname

    # Validate snake_url
    if data.get('snake_url'):
        team.snake_url = data.get('snake_url')

    # Validate is_public
    team.is_public = True if data.get('is_public') else False

    # Validate member_emails
    email = data.get('add_member')
    if email and email not in team.member_emails:
        team.member_emails.append(email)

    # Validate password
    if data.get('password'):
        team.set_password(data.get('password'))

    # Validate game_mode
    if data.get('game_mode') in Game.MODE_VALUES:
        team.game_mode = data.get('game_mode')

    # Validate type
    if is_admin and data.get('type') in Team.TYPE_VALUES:
        team.type = data.get('type')

    team.save()

    flash('Team updated')
    return redirect(request.url)


@app.route('/api/teams/')
def teams_list():
    """
    List all public teams as well as the current team (whether it's public or not).
    Sample response:
    {
      "data": [
        {
          "teamname": "TEAM1",
          "member_emails": ["user@domain.com"],
          "snake_url": "http://localhost:6000/"
        }
      ]
    }
    """
    teams = Team.find(
        {'$or': [
            {'$and': [
                {'is_public': True},
                {'type': {'$ne': Team.TYPE_ADMIN}},
            ]},
            {'_id': g.team.id}
        ]}, limit=50)
    return json_response([team.serialize() for team in teams])


@app.route('/api/teams/current')
def team_info():
    """
    Get information about the current signed in team.

    Sample response:
    {
      "teamname": "TEAM1",
      "member_emails": ["user@domain.com"],
      "snake_url": "http://localhost:6000/"
    }
    """
    app.logger.info(session)
    return json_response(data=g.team.serialize())
