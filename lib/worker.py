# import time
# import os

# from pymongo import MongoClient

# client = MongoClient(os.environ['MONGOLAB_URI'])
# db = client.get_default_database()


# def run_game(game):
#     print 'Running game %s' % game


# def check_for_games():
#     games = db.games.find({'status': 'waiting'}).sort('-created').limit(1)
#     if games.count():
#         run_game(games[0])
#         return True
#     else:
#         print 'No Games'
#         return False

import time

import lib.game.controller as controller
from lib.game.models import Game


def _log(msg):
    print "[worker] %s" % str(msg)


def maybe_run_game():
    _log('looking for games...')
    game_to_run = Game.find_one({'state': Game.STATE_READY})
    if game_to_run:
        _log("running game: %s" % game_to_run.id)
        controller.run_game(game_to_run)
        _log("finished game: %s" % game_to_run.id)
    else:
        _log('no games to run')




def fake_game():
    snakes = [
        {
            'id': 'snake_1',
            'name': 'Cool Snake',
            'color': 'green',
            'coords': [(1, 1), (1, 1)],
            'status': 'alive',
            'url': 'http://battlesnake-go.herokuapp.com'
        },
        {
            'id': 'snake_2',
            'name': 'Stupid Snake',
            'color': 'red',
            'coords': [(3, 3), (3, 3)],
            'status': 'alive',
            'url': 'http://battlesnake-go.herokuapp.com/mk1'
        }
    ]

    controller.create_game(snakes, 10, 10)






def main():
    # fake_game()
    while True:
        maybe_run_game()
        time.sleep(1)


if __name__ == "__main__":
    main()
