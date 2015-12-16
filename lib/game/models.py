import logging

from datetime import datetime

import pymongo

from lib.mongo import get_mongodb
from lib.redis import Queue
from lib.words import get_noun, get_adjective


logger = logging.getLogger(__name__)


class Model(object):

    def __init__(self):
        self.id = None
        self.created = None
        self.modified = None

    def __unicode__(self):
        return '%s[%s]' % (self.__class__.__name__, self.id)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __repr__(self):
        return self.__str__()

    def _add_timestamps(self, obj):
        self.created = obj['created']
        self.modified = obj['modified']

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

    def to_dict(self):
        raise NotImplementedError

    @classmethod
    def _get_collection(cls):
        return get_mongodb()[cls.__name__.lower()]

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

    @classmethod
    def from_dict(cls, result):
        raise NotImplementedError


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
            stats=None,
            turn_time=2.0,
            is_live=True):

        super(Game, self).__init__()

        self.id = id or Game._generate_id()
        self.state = state
        self.stats = stats or {}
        self.width = width
        self.height = height
        self.turn_time = turn_time
        self.is_live = is_live

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

    def mark_ready(self):
        """
        Mark game as ready for a worker to process
        """

        self.state = Game.STATE_READY
        self.save()
        self.ready_queue.enqueue(self.id)

    @staticmethod
    def _generate_id():
        return '%s-%s' % (get_adjective(), get_noun())

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

        instance._add_timestamps(obj)
        return instance


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

        super(GameState, self).__init__()

        self.id = None
        self.game_id = game_id
        self.width = width
        self.height = height
        self.turn = 0
        self.is_done = False
        self.snakes = []
        self.dead_snakes = []
        self.food = []

    def insert(self):
        if not self.id:
            self.id = '%s-%s' % (self.game_id, self.turn)
        return super(GameState, self).insert()

    def generate_board(self):
        board = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append({'state': GameState.TILE_STATE_EMPTY})
            board.append(row)

        for snake in self.snakes:
            for i, coord in enumerate(snake['coords']):
                if i == 0:
                    board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_SNAKE_HEAD
                else:
                    board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_SNAKE_BODY
                board[coord[0]][coord[1]]['snake'] = snake['name']

        for coord in self.food:
            board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_FOOD

        return board

    def sanity_check(self):
        if not isinstance(self.game_id, basestring):
            raise ValueError('Sanity Check Failed: game_id not int, %s' % self.game_id)
        if not isinstance(self.turn, int):
            raise ValueError('Sanity Check Failed: turn is not int, %s' % self.turn)

        for snake in self.snakes:
            for coord in snake['coords']:
                for check_snake in self.snakes:
                    if snake['name'] == check_snake['name']:
                        continue
                    if coord in check_snake['coords']:
                        raise ValueError('Sanity Check Failed: board.snakes contains overlapping coords.')
                if coord in self.food:
                    raise ValueError('Sanity Check Failed: board.snakes and board.food contain overlapping coords.')
                if coord[0] > (self.width - 1):
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[0] < 0:
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[1] > (self.height - 1):
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')
                if coord[1] < 0:
                    raise ValueError('Sanity Check Failed: board.snakes outside bounds of self.board')

    def to_dict(self):
        return {
            '_id': self.id,
            'game_id': self.game_id,
            'is_done': self.is_done,
            'turn': self.turn,
            'snakes': self.snakes[:],
            'dead_snakes': self.dead_snakes[:],
            'food': self.food[:],
            'width': self.width,
            'height': self.height,

            # TODO: Remove the need to have this here
            'board': self.generate_board(),
        }

    @classmethod
    def from_dict(cls, obj):
        game_state = cls(obj['game_id'], obj['width'], obj['height'])
        game_state.id = obj['_id']
        game_state.turn = obj['turn']
        game_state.is_done = obj['is_done']
        game_state.snakes = obj['snakes']
        game_state.dead_snakes = obj['dead_snakes']
        game_state.food = obj['food']

        game_state.sanity_check()

        return game_state


class Team(Model):

    def __init__(self, teamname):
        super(Team, self).__init__()

        self.teamname = teamname

    def is_active(self):
        return True

    def get_id(self):
        return self.teamname

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, password):
        return password == 'password'

    def to_dict(self):
        return {
            'teamname': self.teamname,
        }

    @classmethod
    def from_dict(cls, obj):
        return cls(obj['teamname'])


# Create default team for testing if one doesn't exist
default_team = Team.find_one({'teamname': 'default'})
if not default_team:
    default_team = Team('default')
    default_team.save()
