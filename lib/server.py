import bottle

from bottle import request

from lib.game import Game


def _json_response(data):
    return {
        'data': data,
        'status': 'OK'
    }


@bottle.get('/')
def index():
    return bottle.static_file('html/index.html', root='static')


@bottle.get('/<page>')
def page(page):
    return bottle.static_file('html/%s.html' % page, root='static')


@bottle.get('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


@bottle.post('/api/games')
def games_create():

    width = request.query.get('w', 10)
    height = request.query.get('h', 10)

    game = Game(width=width, height=height)
    game.insert()

    return _json_response(game.to_json())


@bottle.get('/api/games')
def games_list():
    games = Game.find()
    data = []
    for game in games:
        obj = game.to_json()
        data.append(obj)

    return _json_response(data)

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
else:
    app = bottle.default_app()
