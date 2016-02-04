from flask import (
    request, g, session,
    render_template, redirect, url_for, flash,
    abort,
)
from flask.ext.login import login_user
from pymongo.errors import DuplicateKeyError

from lib.server import form_error, json_response, json_error, app
from lib.models.game import Game
from lib.models.team import Team
from lib.routes.auth import admin_only

import lib.ai as ai
import lib.game.engine as engine

@app.route('/team', methods=['GET'])
def get_team():
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team

    # Admin override
    admin_override_id = request.args.get('admin_override_id', None)
    if admin_override_id and is_admin:
        team = Team.find_one({'_id': admin_override_id})
        if not team:
            abort(500)

    return render_template('team.html', team=team, is_admin=is_admin)


@app.route('/team', methods=['POST'])
def post_team():
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    team = g.team
    data = request.form

    # Admin override
    admin_override_id = request.args.get('admin_override_id', None)
    if admin_override_id and is_admin:
        team = Team.find_one({'_id': admin_override_id})
        if not team:
            abort(500)

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
    return redirect(url_for('get_team', admin_override_id=admin_override_id))


@app.route('/team/test', methods=['GET'])
def team_test():
    team = g.team

    # Fake a game
    game = Game(10, 10, 1)
    snakes = [engine.Snake(g.team.snake_url)]
    game_state = engine.Engine.create_game_state(game.id, game.width, game.height)
    engine.Engine.add_random_snakes_to_board(game_state, snakes)

    results = {
        'whois': ai.whois(snakes)[0],
        'start': ai.start(game, game_state)[0],
        'move': ai.move(game, game_state)[0],
        'end': ai.end(game, game_state)[0]
    }

    return render_template('team_test.html', team=team, results=results)


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
    app.logger.info(session)
    return json_response(data=g.team.serialize())


# TODO remove this?
@app.route('/api/teams/current', methods=['PUT'])
def team_update():
    team = g.team
    data = request.get_json()
    if not data:
        return json_error(msg='Invalid team data', status=400)
    if data.has_key('is_public') and not isinstance(data['is_public'], bool):
        return json_error(msg='is_public must be a boolean or omitted', status=400)

    # TODO: check for duplicate team name and allow updating
    for field in ['snake_url', 'is_public']:
        if field in data:
            setattr(team, field, data[field])

    # Handling checkboxes is weird
    team.is_public = True if data.get('is_public') else False

    team.save()
    data = team.serialize()

    # Log in team again in case team name changed
    # Note: calling this seems to make team un-serializable
    login_user(team)

    return json_response(data=data)


# TODO remove this?
@app.route('/api/teams/current/members/<email>', methods=['PUT'])
def team_member_create(email):
    """
    Add a new member to an existing team.
    Sample request:
    PUT /api/teams/current/members/user2@domain.com
    Sample response:
    HTTP 201
    {
      "data": {
        "_id": "TEAM1",
        "member_emails": ["user@domain.com", "user2@domain.com"],
        "snake_url": "http://localhost:6000/"
      },
      "message": "Member added"
    }
    """

    if email not in g.team.member_emails:
        g.team.member_emails.append(email)

        g.team.save()

        return json_response(g.team.member_emails, msg='Member added', status=201)

    return json_response(g.team.member_emails, msg='Member already exists', status=200)


# TODO remove this?
@app.route('/api/teams/<teamname>')
@admin_only
def team_details(teamname):
    """
    Get data for a single team.
    Sample response:
    {
      "data": {
        "_id": "TEAM1",
        "member_emails": ["user@domain.com"],
        "snake_url": "http://localhost:6000/"
      }
    }
    """
    team = Team.find_one({'teamname': teamname})
    if not team:
        return json_error(msg='Team not found', status=404)
    return json_response(team.serialize())


# TODO remove this?
@app.route('/api/teams/', methods=['POST'])
@admin_only
def teams_create():
    """
    Create a new team and return it.
    Sample request:
    POST /api/teams/
    {
      "teamname": "TEAM1",
      "snake_url": "http://localhost:6000/"
      "member_emails": ["user@domain.com"],
    }
    Sample response:
    HTTP 201
    {
      "data": {
        "teamname": "TEAM1",
        "member_emails": ["user@domain.com"],
        "snake_url": "http://localhost:6000/"
      },
      "message": "Team created"
    }
    """
    data = request.get_json()
    if not data:
        return json_error(msg='Invalid team', status=400)

    try:
        teamname = data['teamname']
        password = data['password']
    except KeyError:
        return json_error(msg='Invalid team, missing attributes', status=400)

    snake_url = data.get('snake_url', None)
    member_emails = data.get('member_emails', [])

    existing_team = Team.find_one({'teamname': teamname})
    if existing_team:
        return json_error(msg='Team name already exists', status=400)

    team = Team(teamname=teamname, password=password,
                snake_url=snake_url, member_emails=member_emails)
    try:
        team.insert()
    except DuplicateKeyError:
        return json_error(msg='Team with that name already exists', status=400)

    return json_response(team.serialize(), msg='Team created', status=201)
