from flask import (
    Flask,
    request,
    jsonify, send_from_directory,
)

from lib.game.models import Game, GameState
from lib.game import controller


# Use hardcoded app name to ensure lib is not used for top-level directory
app = Flask('battlesnake')


def _json_response(data={}, msg=None, status=200):
    return jsonify(
        data=data,
        message=msg,
    ), status, {'Content-Type': 'application/json'}


def _json_error(msg=None, status=400):
    return jsonify(message=msg), status, {'Content-Type': 'application/json'}


@app.route('/')
def index():
    return app.send_static_file('html/index.2015.html')


@app.route('/play/')
@app.route('/play/<path:path>')
def page(path=None):
    # serve play.html for anything that starts with "play/"
    # frontend will show the correct route
    return app.send_static_file('html/play.html')


@app.route('/static/<path:path>')
def server_static(path):
    # Flask has this built-in, but it's only active in dev
    return send_from_directory('static', path)


@app.route('/api/games', methods=['POST'])
def games_create():
    data = request.get_json()

    if data is None:
        return _json_response(msg='Invalid request body', status=400)

    width = data.get('width', 20)
    height = data.get('height', 20)
    turn_time = data.get('turn_time', 1)

    try:
        snake_urls = data['snake_urls']
    except KeyError:
        return _json_response(msg='Invalid snakes', status=400)

    try:
        game, game_state = controller.create_game(
            width=width,
            height=height,
            snake_urls=snake_urls,
            turn_time=turn_time
        )
    except Exception as e:
        return _json_response({
            'error': True,
            'message': str(e)
        })

    return _json_response({
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
        return _json_error(str(e))

    return _json_response(game.to_dict())


@app.route('/api/games/<game_id>/rematch', methods=['POST'])
def game_rematch(game_id):
    try:
        game = controller.rematch_game(game_id)
    except Exception as e:
        return _json_error(str(e))

    return _json_response(game.to_dict())


@app.route('/api/games/<game_id>/pause', methods=['PUT'])
def game_pause(game_id):
    game = Game.find_one({'_id': game_id})
    game.state = Game.STATE_PAUSED
    game.save()
    return _json_response(game.to_dict())


@app.route('/api/games/<game_id>/resume', methods=['PUT'])
def game_resume(game_id):
    game = Game.find_one({'_id': game_id})
    game.mark_ready()
    return _json_response(game.to_dict())


@app.route('/api/games/<game_id>/turn', methods=['POST'])
def game_turn(game_id):
    game = Game.find_one({'_id': game_id})
    game_state = controller.next_turn(game)

    return _json_response(game_state.to_dict())


@app.route('/api/games')
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

    return _json_response(data)


@app.route('/api/games/<game_id>')
def game_details(game_id):
    game = Game.find_one({'_id': game_id})
    return _json_response(game.to_dict())


@app.route('/api/games/<game_id>/gamestates/<game_state_id>')
def game_states_details(game_id, game_state_id):
    if game_state_id == 'latest':
        game_state = GameState.find({'game_id': game_id}, limit=1)[0]
    else:
        game_state = GameState.find_one({'_id': game_state_id})

    return _json_response(game_state.to_dict())


@app.route('/api/games/<game_id>/gamestates')
def game_states_list(game_id):
    game_states = GameState.find({'game_id': game_id})
    data = []
    for game_state in game_states:
        data.append(game_state.to_dict())
    return _json_response(data)


# Expose WSGI app
application = app
