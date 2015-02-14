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


def main():
    while True:
        maybe_run_game()
        time.sleep(1)


if __name__ == "__main__":
    main()
