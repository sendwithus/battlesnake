import bottle

from bottle import request, abort

from lib.game.models import Game
from lib import controller
from lib.caller import call_endpoints_async


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
    print data

    if data is None:
        return abort(400, 'No request body')

    width = data.get('w', 20)
    height = data.get('h', 20)

    # try:
    #     snake_urls = data['snakes_urls']
    # except KeyError:
    #     return abort(400, 'Invalid snakes')

    # # Call each snake endpoint
    # start_urls = ['%s/%s' % (url, 'start') for url in snake_urls]
    # responses = call_endpoints_async(
    #     payload=None,
    #     urls=start_urls,
    #     timeout=CLIENT_TIMEOUT_SECONDS
    # )
    #
    # # Attach each snake's URL
    # for url, snake in responses.iteritems():
    #     snake['url'] = url
    #
    # # Extract the array of snakes
    # snakes = responses.values()

    snakes = [
        {
            'id': 'snake_1',
            'name': 'Cool Snake',
            'color': 'green',
            'coords': [(1, 1), (1, 1)],
            'status': 'alive',
            'url': 'http://snake_1.herokuapp.com'
        },
        {
            'id': 'snake_2',
            'name': 'Stupid Snake',
            'color': 'red',
            'coords': [(3, 3), (3, 3)],
            'status': 'alive',
            'url': 'http://snake_2.herokuapp.com/mk1'
        }
    ]

    game, game_state = controller.create_game(
        width=width,
        height=height,
        snakes=snakes
    )

    return _json_response({
        'game': game.to_dict(),
        'game_state': game_state.to_dict()
    })


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
