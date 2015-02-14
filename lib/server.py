import bottle

from bottle import request, abort

from lib.game.models import Game
from lib.game import controller


CLIENT_TIMEOUT_SECONDS = 2


def _json_response(data):
    return {
        'data': data,
        'status': 'OK'
    }


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
    data = request.json

    if data is None:
        return abort(400, 'No request body')

    width = data.get('w', 50)
    height = data.get('h', 50)

    try:
        snake_urls = data['snake_urls']
    except KeyError:
        return abort(400, 'Invalid snakes')

    game, game_state = controller.create_game(
        width=width,
        height=height,
        snake_urls=snake_urls
    )

    return _json_response({
        'game': game.to_dict(),
        'game_state': game_state.to_dict()
    })


@bottle.post('/api/games/:game_id/start')
def game_start(game_id):
    data = request.json

    if data is None:
        return abort(400, 'No request body')

    manual = data.get('manual')

    game = controller.start_game(game_id, manual)

    return _json_response(game.to_dict())


@bottle.post('/api/games/:game_id/turn')
def game_turn(game_id):
    game = Game.find_one({'_id': game_id})

    # # Load snake URLs from the game
    # snake_urls = [snake['url'] for snake in game.snakes]
    #
    # # Call each snake endpoint
    # move_urls = ['%s/%s' % (url, 'move') for url in snake_urls]
    # responses = call_endpoints_async(
    #     payload=None,
    #     urls=move_urls,
    #     timeout=CLIENT_TIMEOUT_SECONDS
    # )
    # moves = responses.values()

    moves = [
        {
            'snake_id': 'snake_1',
            'action': 'right'
        },
        {
            'snake_id': 'snake_2',
            'action': 'left'
        }
    ]

    game_state = controller.next_turn(game, moves)

    return _json_response(game_state.to_dict())


@bottle.get('/api/games')
def games_list():
    games = Game.find()
    data = []
    for game in games:
        obj = game.to_dict()
        data.append(obj)

    return _json_response(data)


@bottle.get('/api/games/:game_id')
def game_details(game_id):
    game = Game.find_one({'_id': game_id})
    return _json_response(game.to_dict())

# Expose WSGI app
application = bottle.default_app()
