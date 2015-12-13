import time

import lib.game.controller as controller
from lib.models.game import Game
from lib.log import get_logger


logger = get_logger(__name__)


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
    controller.run_game(game_to_run)
    logger.info('Finished game: %s', game_to_run.id)


def main():
    while True:
        maybe_run_game()
        time.sleep(1)


if __name__ == "__main__":
    main()
