from lib.models.game import Game


def serialize_game(game, game_state=None):
    data = {
        'game': game.id,
        'mode': game.mode,
        'height': game.height,
        'width': game.width,
        'turn': game_state.turn if game_state else 0,
        'snakes': serialize_snakes(game, game_state.snakes) if game_state else [],
        'food': game_state.food
    }

    if game.mode == Game.MODE_ADVANCED:
        data.update({
            'gold': game_state.gold,
            'walls': game_state.walls
        })
    return data


def serialize_snake(game, snake):
    data = {
        'name': snake.name,
        'taunt': snake.taunt,
        'status': snake.status,
        'message': snake.message,
        'age': snake.age,
        'health': snake.health,
        'coords': snake.coords,
        'kills': snake.kills,
    }

    if game.mode == Game.MODE_ADVANCED:
        data.update({
            'gold': snake.gold
        })
    return data


def serialize_snakes(game, snakes):
    return [serialize_snake(game, snake) for snake in snakes]
