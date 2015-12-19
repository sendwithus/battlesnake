from lib.server import _json_response, app

@app.route('/api/tournaments/')
def tournaments_list():
    """ List all tournaments """
    return _json_response([])


@app.route('/api/tournaments/', methods=['POST'])
def tournaments_create():
    """ Create a new tournament and return it """
    return _json_response({}, msg='Tournament created', status=201)


@app.route('/api/tournaments/<tournament_id>')
def tournament_details(tournament_id):
    """ Get data for a single tournament """
    return _json_response(msg='Tournament not found', status=404)


@app.route('/api/tournaments/<tournament_id>/games/')
def tournament_games_list(tournament_id):
    """ List all games in a tournament """
    return _json_response([])


@app.route('/api/tournaments/<tournament_id>/games/', methods=['POST'])
def tournament_game_create(tournament_id):
    """ Add a new game to an existing tournament """
    return _json_response({}, msg='Game created', status=201)


@app.route('/api/tournaments/<tournament_id>/games/<game_id>')
def tournament_game_detail(tournament_id, game_id):
    """ List an individual game in a tournament with additional
    tournament-related metadata (e.g. game number) """
    return _json_response(msg='Game not found', status=404)
