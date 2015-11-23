import logging

from datetime import datetime

import pymongo

from lib.mongo import get_mongodb
from lib.redis import Queue
from lib.words import get_noun, get_adjective


logger = logging.getLogger(__name__)


class Model(object):

    def __unicode__(self):
        return '%s[%s]' % (self.__class__.__name__, self.id)

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return self.__unicode__().encode('utf-8')
        else:
            return super(Game, self).__str__()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def _get_collection(cls):
        return get_mongodb()[cls.__name__.lower()]

    def refetch(self):
        return self.find_one({'_id': self.id})

    def insert(self):
        doc = self.to_dict()
        doc['modified'] = datetime.now()
        doc['created'] = doc.get('created', datetime.now())
        self._get_collection().insert(doc)

    def save(self):
        doc = self.to_dict()
        doc['modified'] = datetime.now()
        doc['created'] = self.created
        self._get_collection().update({'_id': self.id}, doc, True)

    def add_timestamps(self, obj):
        self.created = obj['created']
        self.modified = obj['modified']

    @classmethod
    def find(cls, *args, **kwargs):
        results = cls._get_collection().find(
            *args,
            sort=[('created', pymongo.DESCENDING)],
            **kwargs)

        objects = []

        for result in results:
            obj = cls.from_dict(result)
            objects.append(obj)

        return objects

    @classmethod
    def find_one(cls, *args, **kwargs):
        doc = cls._get_collection().find_one(*args, **kwargs)
        if doc:
            return cls.from_dict(doc)
        return None


class Game(Model):
    STATE_CREATED = 'created'
    STATE_PAUSED = 'paused'
    STATE_MANUAL = 'manual'
    STATE_READY = 'ready'
    STATE_PLAYING = 'playing'
    STATE_DONE = 'done'

    ready_queue = Queue('games:ready')

    def __init__(
            self,
            id=None,
            width=10,
            height=10,
            state=STATE_CREATED,
            stats={},
            turn_time=2.0,
            is_live=True):

        self.id = id or self._generate_id()
        self.state = state
        self.stats = stats
        self.width = width
        self.height = height
        self.turn_time = turn_time
        self.is_live = is_live

    def _generate_id(self):
        return '%s-%s' % (get_adjective(), get_noun())

    def to_dict(self):
        return {
            '_id': self.id,
            'state': self.state,
            'stats': self.stats,
            'width': self.width,
            'height': self.height,
            'turn_time': self.turn_time,
            'is_live': self.is_live
        }

    @classmethod
    def from_dict(cls, obj):
        instance = cls(
            id=obj['_id'],
            state=obj['state'],
            width=obj['width'],
            stats=obj['stats'],
            height=obj['height'],
            turn_time=obj['turn_time'],
            is_live=obj.get('is_live', False)
        )

        instance.add_timestamps(obj)
        return instance

    def mark_ready(self):
        """ Marks this game as ready for a worker to process """
        self.state = Game.STATE_READY
        self.save()
        self.ready_queue.enqueue(self.id)


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

    def __init__(self, game_id):
        self.id = None
        self.game_id = game_id
        self.turn = 0
        self.is_done = False
        self.board = []
        self.snakes = []
        self.dead_snakes = []
        self.food = []

    def insert(self):
        if not self.id:
            self.id = '%s-%s' % (self.game_id, self.turn)
        return super(GameState, self).insert()

    def sanity_check(self):
        if not isinstance(self.game_id, basestring):
            raise ValueError('Sanity Check Failed: game_id not int, %s' % self.game_id)
        if not isinstance(self.turn, int):
            raise ValueError('Sanity Check Failed: turn is not int, %s' % self.turn)

        # Board State
        if not isinstance(self.board, list):
            raise ValueError('Sanity Check Failed: board is not list, %s' % self.board)
        row_size = None
        for tile_row in self.board:
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
                    raise ValueError('Sanity Check Failed: board.tile has invalid state, %s' % (
                        tile['state']))

        for snake in self.snakes:
            for coord in snake['coords']:
                for check_snake in self.snakes:
                    if snake['name'] == check_snake['name']:
                        continue
                    if coord in check_snake['coords']:
                        raise ValueError('Sanity Check Failed: board.snakes contains overlapping coords.')
                if coord in self.food:
                    raise ValueError('Sanity Check Failed: board.snakes and board.food contain overlapping coords.')
                if coord[0] > (len(self.board) - 1):
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[0] < 0:
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[1] > (len(self.board[0]) - 1):
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[1] < 0:
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')

    # Serialize/Deserialize

    def to_dict(self):
        return {
            '_id': self.id,
            'game_id': self.game_id,
            'is_done': self.is_done,
            'turn': self.turn,
            'board': self.board[:],
            'snakes': self.snakes[:],
            'dead_snakes': self.dead_snakes[:],
            'food': self.food[:]
        }

    def to_string(self):
        self.sanity_check()

        tile_map = {
            GameState.TILE_STATE_EMPTY: '_',
            GameState.TILE_STATE_FOOD: '*',
            GameState.TILE_STATE_SNAKE_BODY: 'B',
            GameState.TILE_STATE_SNAKE_HEAD: 'H'
        }

        output = ''

        for y in range(len(self.board[0])):
            for x in range(len(self.board)):
                output += tile_map[self.board[x][y]['state']]
            output += '\n'
        output += '\n'

        return output

    def from_string(self, content):
        self.board = []

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
            self.board.append(row)

        self.sanity_check()

    @classmethod
    def from_dict(cls, obj):
        game_state = cls(obj['game_id'])
        game_state.id = obj['_id']
        game_state.turn = obj['turn']
        game_state.is_done = obj['is_done']
        game_state.board = obj['board']
        game_state.snakes = obj['snakes']
        game_state.dead_snakes = obj['dead_snakes']
        game_state.food = obj['food']

        game_state.sanity_check()

        return game_state
