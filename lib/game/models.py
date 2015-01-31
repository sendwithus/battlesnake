import logging
from datetime import datetime

from pymongo import MongoClient

logger = logging.getLogger(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['battlesnake']


class Model(object):

    def _get_collection(self):
        return db[self.__class__.__name__.lower()]

    def insert(self):
        doc = self.to_json()
        doc['modified'] = datetime.now()
        doc['created'] = doc.get('created', datetime.now())
        self._get_collection().insert(doc)

    def find(self, *args, **kwargs):
        return self._get_collection().find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self._get_collection().find_one(*args, **kwargs)


class Game(Model):
    STATE_CREATED = 'created'
    STATE_READY = 'ready'
    STATE_PLAYING = 'playing'
    STATE_DONE = 'done'

    def __init__(self, id=None, width=10, height=10, state=STATE_CREATED):
        self._id = id or self._generate_game_id()
        self._state = state
        self._width = width
        self._height = height

    def _generate_game_id(self):
        return 'need-to-make-ids-still'

    def to_json(self):
        return {
            '_id': self._id,
            'state': self._state,
            'width': self._width,
            'height': self._height
        }

    @staticmethod
    def from_json(cls, obj):
        return cls(
            id=obj['_id'],
            state=obj['state'],
            width=obj['width'],
            height=obj['height']
        )


class GameState(Model):
    TILE_STATE_EMPTY = 'empty'
    TILE_STATE_FOOD = 'food'
    TILE_STATE_SNAKE_HEAD = 'head'
    TILE_STATE_SNAKE_BODY = 'body'

    TILE_STATES = [
        TILE_STATE_EMPTY,
        TILE_STATE_SNAKE_HEAD,
        TILE_STATE_SNAKE_BODY,
        TILE_STATE_FOOD
    ]

    def __init__(self, game_id, width, height):

        self._game_id = game_id
        self._board = []
        for x in range(width):
            self._board.append([])
            for y in range(height):
                self._board[x].append({
                    'state': GameState.TILE_STATE_EMPTY,
                    'snake': None
                })

        self._snakes = []
        self._turn = 0

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
                if tile['state'] not in GameState.TILE_STATES:
                    raise ValueError('Sanity Check FaileD: board.tile has invalid state, %s' % (
                        tile['state']))

        # TODO: Sanity check snakes array

    # Serialize/Deserialize

    def to_json(self):
        return {
            'game_id': self._game_id,
            'turn': self._turn,
            'board': self._board[:],
            'snakes': self._snakes[:]
        }

    def from_json(self, obj):
        self._game_id = obj['game_id']
        self._turn = obj['turn']
        self._board = obj['board']
        self._snakes = obj['snakes']

        self._sanity_check()

    def to_string(self):
        self._sanity_check()

        tile_map = {
            GameState.TILE_STATE_EMPTY: '_',
            GameState.TILE_STATE_FOOD: '*',
            GameState.TILE_STATE_SNAKE_BODY: 'B',
            GameState.TILE_STATE_SNAKE_HEAD: 'H'
        }

        output = ''
        for row in self._board:
            for tile in row:
                output += tile_map[tile['state']]
            output += '\n'
        output += '\n'

        return output

    def from_string(self, content):
        self._board = []

        tile_map = {
            '_': GameState.TILE_STATE_EMPTY,
            '*': GameState.TILE_STATE_FOOD,
            'B': GameState.TILE_STATE_SNAKE_BODY,
            'H': GameState.TILE_STATE_SNAKE_HEAD
        }

        for raw_row in [row for row in content.split('\n') if row]:
            row = []

            for raw_tile in raw_row:
                row.append({
                    'state': tile_map[raw_tile],
                    'snake': None
                })
            self._board.append(row)

        self._sanity_check()
