import bottle


@bottle.get('/')
def index():
    return bottle.static_file('html/index.html', root='static')


@bottle.get('/<page>')
def page(page):
    return bottle.static_file('html/%s.html' % page, root='static')


@bottle.get('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='static')


if __name__ == '__main__':
    bottle.run(host='localhost', port=8080)
else:
    app = bottle.default_app()
