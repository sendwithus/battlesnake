import time

import newrelic.agent

import lib.game.controller as controller
from lib.log import get_logger
from lib.models.game import Game


logger = get_logger(__name__)


def patch_gevent():
    try:
        import gevent.monkey
    except ImportError:
        raise RuntimeError('gevent is required for lib.worker')
    gevent.monkey.patch_all(thread=False)


def maybe_run_game():
    game_id = Game.ready_queue.dequeue(timeout=60)
    if not game_id:
        logger.info('No game is ready')
        return

    game_to_run = Game.find_one({'_id': game_id})
    if not game_to_run:
        logger.warning('Game not found: %s', game_id)
        return

    logger.info('Running game: %s', game_to_run.id)
    run_game(game_to_run)
    logger.info('Finished game: %s', game_to_run.id)


@newrelic.agent.background_task(name='run_game', group='Worker')
def run_game(game_to_run):
    controller.run_game(game_to_run)


def main():
    patch_gevent()

    while True:
        maybe_run_game()
        time.sleep(1)


if __name__ == "__main__":
    main()
