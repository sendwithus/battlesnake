
def serialize_game(game, game_state=None):
    return {
        'game': game.id,
        'mode': game.mode,
        'height': game.height,
        'width': game.width,
        'turn': game_state.turn if game_state else 0,
        'snakes': serialize_snakes(game_state.snakes) if game_state else [],
        'food': game_state.food,
        'gold': game_state.gold
    }


def serialize_snake(snake):
    return {
        'name': snake.name,
        'taunt': snake.taunt,
        'status': snake.status,
        'message': snake.message,
        'age': snake.age,
        'health': snake.health,
        'coords': snake.coords,
        'kills': snake.kills,
    }


def serialize_snakes(snakes):
    return [serialize_snake(snake) for snake in snakes]
