import time

import lib.game.controller as controller
from lib.game.models import Game


def _log(msg):
    print "[worker] %s" % str(msg)


def maybe_run_game():
    game_id = Game.ready_queue.dequeue(timeout=60)
    if not game_id:
        _log("no game is ready")
        return

    game_to_run = Game.find_one({'_id': game_id})
    if not game_to_run:
        _log("game not found: %s" % game_id)
        return

    _log("running game: %s" % game_to_run.id)
    controller.run_game(game_to_run)
    _log("finished game: %s" % game_to_run.id)


def main():
    while True:
        maybe_run_game()
        time.sleep(1)


if __name__ == "__main__":
    main()
