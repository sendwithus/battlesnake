from flask import request, g, render_template

import lib.ai as ai
import lib.game.engine as engine
from lib.models.game import Game
from lib.server import app


@app.route('/test', methods=['GET'])
def test_snake():
    snake_url = request.args.get('url')
    if not snake_url:
        snake_url = g.team.snake_url

    # Fake a game
    game = Game(10, 10, 1)
    snakes = [engine.Snake('test-snake-id', snake_url)]
    game_state = engine.Engine.create_game_state(game.id, game.width, game.height)
    engine.Engine.add_random_snakes_to_board(game_state, snakes)

    results = {
        'whois': ai.whois(snakes)[0],
        'start': ai.start(game, game_state)[0],
        'move': ai.move(game, game_state)[0],
        'end': ai.end(game, game_state)[0]
    }

    return render_template('test.html', snake_url=snake_url, results=results)
