import random
import time

import newrelic.agent
import sys

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


def maybe_run_game(mode):
    # Get queue by mode. If invalid mode, select random queue
    queue = Game.queues.get(
        mode,
        random.choice(Game.queues.values())
    )

    game_id = queue.dequeue(timeout=60)

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


def main(mode=None):
    patch_gevent()

    while True:
        maybe_run_game(mode=mode)
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
