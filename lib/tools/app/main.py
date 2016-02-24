import bottle
import json
import os
from lib.tools.app.SnakeIMPL import SimpleSnake
from snakes.brad import Snake as BradSnake
# from app.BradSnake import Snake as BradSnake
from snakes.chicken import Snake as ChickenSnake
# from app.ChickenSnake import Snake as ChickenSnake
from snakes.curtisss import Snake as CurtisSnake
# from app.CurtisSnake import Snake as CurtisSnake
from snakes.greg import Snake as GregSnake
# from app.GregSnake import Snake as GregSnake

__snake = None
__SNAKES = {'SimpleSnake': SimpleSnake(),
            'GregSnake': GregSnake(),
            'CurtisSnake': CurtisSnake(),
            'ChickenSnake': ChickenSnake(),
            'BradSnake': BradSnake()
            }
__PORT = os.environ.get("PORT", 8080)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # could pass the head_url ?
    return __snake.whois()


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return __snake.start(data)  # returns a taunt only :)
    """
    return {
        'taunt': 'battlesnake-python!'
    }
    """


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    print "/move data type: %s" % type(data)
    print "/move data: %s" % json.dumps(data)
    return __snake.move(data)  # returns a move and a taunt
    """
    return {
        'move': 'north',
        'taunt': 'battlesnake-python!'
    }
    """


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return __snake.end(data)  # what ever is returned gets ignored
    """
    return {
        'taunt': 'battlesnake-python!'
    }
    """


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    if __snake is None:
        __snake = __SNAKES['CurtisSnake']
        # __snake = __SNAKES['GregSnake']
        # __snake = __SNAKES['ChickenSnake']
        # print type(__snake)

    # bottle.run(application, host='127.0.0.1', port=8080)
    bottle.run(application, host='0.0.0.0', port=__PORT)
