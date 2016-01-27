from flask import request

from lib.log import get_logger
from lib.models.game import Game, GameState
from lib.models.team import Team
from lib.game import controller
from lib.server import json_response, json_error, app

logger = get_logger(__name__)


@app.route('/api/games', methods=['POST'])
def games_create():
    data = request.get_json()

    if data is None:
        return json_response(msg='Invalid request body', status=400)

    width = data.get('width', 20)
    height = data.get('height', 20)
    turn_time = data.get('turn_time', 1)
    mode = data.get('mode', Game.MODE_CLASSIC)

    team_dicts = data['teams']

    # Add all team snake URLs to snake_urls
    snake_urls = []
    teams = []
    for team_dict in team_dicts:
        team = Team.find_one({'_id': team_dict['_id']})
        if not team:
            return json_response(msg='Team not found', status=404)
        if not team.ready_to_play():
            error = 'Team "%s" is not ready to play' % team.teamname
            return json_error(error)

        teams.append(team)
        snake_urls.append(team.snake_url)

    try:
        game, game_state = controller.create_game(
            width=width,
            height=height,
            snake_urls=snake_urls,
            turn_time=turn_time,
            mode=mode
        )
    except Exception as e:
        return json_error(e)

    # Add the game ID to the team's list of games
    for team in teams:
        team.game_ids.append(game.id)
        team.save()

    return json_response({
        'game': game.to_dict(),
        'game_state': game_state.to_dict()
    })


@app.route('/api/games/<game_id>/start', methods=['POST'])
def game_start(game_id):
    data = request.get_json()

    manual = data.get('manual')

    try:
        game = controller.start_game(game_id, manual)
    except Exception as e:
        return json_error(e)

    return json_response(game.to_dict())


@app.route('/api/games/<game_id>/rematch', methods=['POST'])
def game_rematch(game_id):
    try:
        game = controller.rematch_game(game_id)
    except Exception as e:
        return json_error(e)

    return json_response(game.to_dict())


@app.route('/api/games/<game_id>/pause', methods=['PUT'])
def game_pause(game_id):
    game = Game.find_one({'_id': game_id})
    game.state = Game.STATE_PAUSED
    game.save()
    return json_response(game.to_dict())


@app.route('/api/games/<game_id>/resume', methods=['PUT'])
def game_resume(game_id):
    game = Game.find_one({'_id': game_id})
    game.mark_ready()
    return json_response(game.to_dict())


@app.route('/api/games/<game_id>/turn', methods=['POST'])
def game_turn(game_id):
    game = Game.find_one({'_id': game_id})
    game_state = controller.next_turn(game)

    return json_response(game_state.to_dict())


@app.route('/api/games', methods=['GET'])
def games_list():
    games = Game.find({
        'is_live': True,
        'state': {
            '$in': [
                Game.STATE_PLAYING,
                Game.STATE_DONE
            ]
        }
    }, limit=50)

    data = []
    for game in games:
        obj = game.to_dict()
        data.append(obj)

    return json_response(data)


@app.route('/api/games/<game_id>')
def game_details(game_id):
    game = Game.find_one({'_id': game_id})
    if game:
        return json_response(game.to_dict())
    else:
        return json_response()


@app.route('/api/games/<game_id>/gamestates/<game_state_id>')
def game_states_details(game_id, game_state_id):
    if game_state_id == 'latest':
        game_state = GameState.find({'game_id': game_id}, limit=1)[0]
    else:
        game_state = GameState.find_one({'_id': game_state_id})

    return json_response(game_state.to_dict())


@app.route('/api/games/<game_id>/gamestates')
def game_states_list(game_id):
    game_states = GameState.find({'game_id': game_id})
    data = []
    for game_state in game_states:
        data.append(game_state.to_dict())
    return json_response(data)
