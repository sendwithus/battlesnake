from flask import g, request, session
from flask.ext.login import login_required, login_user
from pymongo.errors import DuplicateKeyError

from lib.server import json_response, json_error, app
from lib.models.team import Team

# Public routes


@app.route('/api/teams/')
def teams_list():
    """
    List all teams.
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
    teams = Team.find({}, limit=50)
    return json_response([team.serialize() for team in teams])


@app.route('/api/teams/<teamname>')
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


# Signed in team routes

@app.route('/api/teams/current')
@login_required
def team_info():
    app.logger.info(session)
    return json_response(data=g.team.serialize())


@app.route('/api/teams/current', methods=['PUT'])
@login_required
def team_update():
    team = g.team
    data = request.get_json()
    if not data:
        return json_error(msg='Invalid team data', status=400)

    # TODO: check for duplicate team name and allow updating
    for field in ['snake_url']:
        if field in data:
            setattr(team, field, data[field])

    team.save()
    data = team.serialize()

    # Log in team again in case team name changed
    # Note: calling this seems to make team un-serializable
    login_user(team)

    return json_response(data=data)


@app.route('/api/teams/current/members/<email>', methods=['PUT'])
@login_required
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


@app.route('/api/teams/current/public/<value>', methods=['PUT'])
@login_required
def team_member_public(value):
    """
    Set team is_public flag to <value>
    Sample request:
    PUT /api/teams/TEAM1/members/true
    Sample response:
    HTTP 201
    {
      "data": {
        "_id": "TEAM1",
        ...
        "is_public": true
      },
      "message": "is_public set to 'true'"
    }
    """

    if value not in ['true', 'false']:
        return json_error(msg='Invalid public value. Must be \'true\' or \'false\'', status=400)

    g.team.is_public = (value == 'true')
    g.team.save()

    return json_response(data=g.team.serialize(), msg='Team public set to %s' % value, status=200)


# Super user routes
# TODO: authorization on routes that modify teams

@app.route('/api/teams/', methods=['POST'])
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
