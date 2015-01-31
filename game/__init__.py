import logging


logger = logging.getLogger(__name__)


class GameState(object):
    TILE_STATE_EMPTY = 'empty'
    TILE_STATE_SNAKE_HEAD = 'head'
    TILE_STATE_SNAKE_BODY = 'body'
    TILE_STATE_FOOD = 'food'

    TILE_STATES = [
        TILE_STATE_EMPTY,
        TILE_STATE_SNAKE_HEAD,
        TILE_STATE_SNAKE_BODY,
        TILE_STATE_FOOD
    ]

    def __init__(self, game_id=None, width=10, height=10):
        self._game_id = game_id
        if not self._game_id:
            self._generate_game_id()

        self._board = []
        for x in range(width):
            self._board.append([])
            for y in (height):
                self._board[x].append({
                    'state': GameState.TILE_STATE_EMPTY,
                    'snake': None
                })

        self._snakes = []
        self._turn = 0

    def _generate_game_id(self):
        self._game_id = 'need-to-make-ids-still'

    def _sanity_check(self):
        if not isinstance(self._game_id, basestring):
            raise ValueError('Sanity Check Failed: game_id not int, %s' % self._game_id)
        if not isinstance(self._turn, int):
            raise ValueError('Sanity Check Failed: turn is not int, %s' % self._turn)

        # Board State
        if not isinstance(self._board, list):
            raise ValueError('Sanity Check Failed: board is not list, %s' % self._board)
        row_size = None
        for tile_row in self._board:
            if not isinstance(tile_row, list):
                raise ValueError('Sanity Check Failed: board.tile_row is not list, %s' % (tile_row))

            if not row_size:
                row_size = len(tile_row)
            if len(tile_row) != row_size:
                raise ValueError('Sanity Check Failed: board.tile_row is wrong length')

            for tile in tile_row:
                if not isinstance(tile, dict):
                    raise ValueError('Sanity Check Failed: board.tile is not dict' % (tile))
                if tile['type'] not in GameState.TILE_STATES:
                    raise ValueError('Sanity Check FaileD: board.tile has invalid state, %s' % (
                        tile['type]']))

    def to_json(self):
        return {
            'id': self._game_id,
            'turn': self._turn,
            'board': self._board.copy(),
            'snakes': self._snakes.copy()
        }

    def from_json(self, obj):
        self._game_id = obj['id']
        self._turn = obj['turn']
        self._board = obj['board']
        self._snakes = obj['snakes']

        self._sanity_check()
