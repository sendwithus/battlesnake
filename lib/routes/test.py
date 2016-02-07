from flask import abort, request, g, render_template

import lib.ai as ai
import lib.game.engine as engine
from lib.models.game import Game
from lib.models.team import Team
from lib.server import app


@app.route('/test', methods=['GET'])
@app.route('/admin/test', methods=['GET'])
def test_snake():
    is_admin = (g.team.type == Team.TYPE_ADMIN)
    snake_url = g.team.snake_url

    if is_admin and request.args.get('url'):
        snake_url = request.args.get('url')
    else:
        if 'admin' in request.url:
            abort(404)

    # Fake a game
    game = Game(10, 10, 1)
    snakes = [engine.Snake('test-snake-id', snake_url)]
    game_state = engine.Engine.create_game_state(game.id, game.width, game.height)
    engine.Engine.add_random_snakes_to_board(game_state, snakes)

    results = {
        'info': ai.whois(snakes)[0],
        'start': ai.start(game, game_state)[0],
        'move': ai.move(game, game_state)[0],
        'end': ai.end(game, game_state)[0]
    }

    return render_template('test.html', is_admin=is_admin, snake_url=snake_url, results=results)
