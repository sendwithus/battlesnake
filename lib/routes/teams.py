from flask import Blueprint, request
from pymongo.errors import DuplicateKeyError

from lib.server import _json_response
from lib.models.team import Team


teams = Blueprint('teams', __name__)

# TODO: implement authentication
# TODO: authorization on routes that modify teams

@teams.route('/api/teams/')
def teams_list():
    """
    List all teams.

    Sample response:
    {
      "data": [
        {
          "_id": "TEAM1",
          "member_emails": ["user@domain.com"],
          "snake_url": "http://localhost:6000/"
        }
      ]
    }
    """
    teams = Team.find({}, limit=50)
    return _json_response([team.to_dict() for team in teams])


@teams.route('/api/teams/', methods=['POST'])
def teams_create():
    """
    Create a new team and return it.

    Sample request:
    POST /api/teams/
    {
      "name": "TEAM1",
      "snake_url": "http://localhost:6000/"
      "member_emails": ["user@domain.com"],
    }

    Sample response:
    HTTP 201
    {
      "data": {
        "_id": "TEAM1",
        "member_emails": ["user@domain.com"],
        "snake_url": "http://localhost:6000/"
      },
      "message": "Team created"
    }
    """
    data = request.get_json()
    if not data:
        return _json_response(msg='Invalid team', status=400)

    try:
        name = data['name']
    except KeyError:
        return _json_response(msg='Invalid team', status=400)

    snake_url = data.get('snake_url', None)
    member_emails = data.get('member_emails', [])

    team = Team(name=name, snake_url=snake_url, member_emails=member_emails)
    try:
        team.insert()
    except DuplicateKeyError:
        return _json_response({}, msg='Team with that name already exists', status=400)

    return _json_response(team.to_dict(), msg='Team created', status=201)


@teams.route('/api/teams/<team_name>')
def team_details(team_name):
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
    team = Team.find_one({'_id': team_name})
    if not team:
        return _json_response(msg='Team not found', status=404)
    return _json_response(team.to_dict())


@teams.route('/api/teams/<team_name>/members/<email>', methods=['PUT'])
def team_member_create(team_name, email):
    """
    Add a new member to an existing team.

    Sample request:
    PUT /api/teams/TEAM1/members/user2@domain.com

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
    team = Team.find_one({'_id': team_name})
    if not team:
        return _json_response(msg='Team not found', status=404)

    if email not in team.member_emails:
        team.member_emails.append(email)

        team.save()

        return _json_response(team.member_emails, msg='Member added', status=201)

    return _json_response(team.member_emails, msg='Member already exists', status=200)
