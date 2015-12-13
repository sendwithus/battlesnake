import bottle
import json

from lib.game.models import Game, GameState
from lib.game import controller


def _json_response(data={}, msg=None, status=200):
    body = json.dumps({
        'data': data,
        'message': msg
    })

    return bottle.HTTPResponse(
        body,
        status=status,
        headers={'Content-Type': 'application/json'})


@bottle.get('/')
def index():
    return bottle.static_file('html/index.html', root='static')


@bottle.get('/play<:re:.*>')
def page():
    # serve play.html for anything that starts with "play/"
    # fontend with show the correct route
    return bottle.static_file('html/play.html', root='static')


@bottle.get('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


@bottle.post('/api/games')
def games_create():
    data = bottle.request.json

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


@bottle.post('/api/games/:game_id/start')
def game_start(game_id):
    data = bottle.request.json

    if data is None:
        return bottle.abort(400, 'No request body')

    manual = data.get('manual')

    try:
        game = controller.start_game(game_id, manual)
    except Exception as e:
        return bottle.abort(400, str(e))

    return _json_response(game.to_dict())


@bottle.post('/api/games/:game_id/rematch')
def game_rematch(game_id):
    try:
        game = controller.rematch_game(game_id)
    except Exception as e:
        return bottle.abort(400, str(e))

    return _json_response(game.to_dict())


@bottle.put('/api/games/:game_id/pause')
def game_pause(game_id):
    game = Game.find_one({'_id': game_id})
    game.state = Game.STATE_PAUSED
    game.save()
    return _json_response(game.to_dict())


@bottle.put('/api/games/:game_id/resume')
def game_resume(game_id):
    game = Game.find_one({'_id': game_id})
    game.mark_ready()
    return _json_response(game.to_dict())


@bottle.post('/api/games/:game_id/turn')
def game_turn(game_id):
    game = Game.find_one({'_id': game_id})
    game_state = controller.next_turn(game)

    return _json_response(game_state.to_dict())


@bottle.get('/api/games')
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


@bottle.get('/api/games/:game_id')
def game_details(game_id):
    game = Game.find_one({'_id': game_id})
    return _json_response(game.to_dict())


@bottle.get('/api/games/:game_id/gamestates/:game_state_id')
def game_states_details(game_id, game_state_id):
    if game_state_id == 'latest':
        game_state = GameState.find({'game_id': game_id}, limit=1)[0]
    else:
        game_state = GameState.find_one({'_id': game_state_id})

    return _json_response(game_state.to_dict())


@bottle.get('/api/games/:game_id/gamestates')
def game_states_list(game_id):
    game_states = GameState.find({'game_id': game_id})
    data = []
    for game_state in game_states:
        data.append(game_state.to_dict())
    return _json_response(data)


# Expose a WSGI app for gunicorn to use
application = bottle.default_app()


# Things to run locally
def main():
    # Run a debug server locally
    bottle.run(host='localhost', port=8080, debug=True)  # reloader=True <-- this breaks things

if __name__ == "__main__":
    main()
