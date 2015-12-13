import bottle
from lib.server import _json_response


@bottle.get('/api/teams/')
def teams_list():
    """ List all teams """
    return _json_response([])


@bottle.post('/api/teams/')
def teams_create():
    """ Create a new team and return it """
    return _json_response({}, msg='Team created', status=201)


@bottle.get('/api/teams/:team_name')
def team_details(team_name):
    """ Get data for a single team """
    return _json_response(msg='Team not found', status=404)


@bottle.get('/api/teams/:team_name/members/')
def team_members_list(team_name):
    """ List all members in a team """
    return _json_response([])


@bottle.put('/api/teams/:team_name/members/:email')
def team_member_create(team_name, email):
    """ Add a new member to an existing team """
    return _json_response({}, msg='Member created', status=201)
