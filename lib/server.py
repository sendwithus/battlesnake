import bottle

from bottle import request


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
def games_post():
    from lib.game import Game

    width = request.query.get('w', 10)
    height = request.query.get('h', 10)

    game = Game(width=width, height=height)
    game.insert()

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
else:
    app = bottle.default_app()
