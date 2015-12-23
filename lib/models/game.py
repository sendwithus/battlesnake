import logging

from lib.models.base import Model
from lib.redis_client import Queue
from lib.words import get_noun, get_adjective


logger = logging.getLogger(__name__)


class Game(Model):
    STATE_CREATED = 'created'
    STATE_PAUSED = 'paused'
    STATE_MANUAL = 'manual'
    STATE_READY = 'ready'
    STATE_PLAYING = 'playing'
    STATE_DONE = 'done'

    MODE_CLASSIC = 'classic'

    ready_queue = Queue('games:ready')

    def __init__(
            self,
            id=None,
            width=10,
            height=10,
            state=STATE_CREATED,
            stats=None,
            turn_time=2.0,
            is_live=True,
            mode=MODE_CLASSIC):

        super(Game, self).__init__()

        self.id = id or Game._generate_id()
        self.state = state
        self.stats = stats or {}
        self.width = width
        self.height = height
        self.turn_time = turn_time
        self.is_live = is_live
        self.mode = mode

    def to_dict(self):
        return {
            '_id': self.id,
            'state': self.state,
            'stats': self.stats,
            'width': self.width,
            'height': self.height,
            'turn_time': self.turn_time,
            'is_live': self.is_live,
            'mode': self.mode
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
            is_live=obj.get('is_live', False),
            mode=obj.get('mode', cls.MODE_CLASSIC)
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
            for i, coord in enumerate(snake.coords):
                if i == 0:
                    board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_SNAKE_HEAD
                else:
                    board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_SNAKE_BODY
                board[coord[0]][coord[1]]['snake'] = snake.name

        for coord in self.food:
            board[coord[0]][coord[1]]['state'] = GameState.TILE_STATE_FOOD

        return board

    def sanity_check(self):
        if not isinstance(self.game_id, basestring):
            raise ValueError('Sanity Check Failed: game_id not int, %s' % self.game_id)
        if not isinstance(self.turn, int):
            raise ValueError('Sanity Check Failed: turn is not int, %s' % self.turn)

        for snake in self.snakes:
            for coord in snake.coords:
                for check_snake in self.snakes:
                    if snake.url == check_snake.url:
                        continue
                    if coord in check_snake.coords:
                        raise ValueError('board.snakes contains overlapping coords.')
                if coord in self.food:
                    raise ValueError('board.snakes and board.food contain overlapping coords.')
                if coord[0] > (self.width - 1):
                    raise ValueError('board.snakes outside bounds of self.board')
                if coord[0] < 0:
                    raise ValueError('board.snakes outside bounds of self.board')
                if coord[1] > (self.height - 1):
                    raise ValueError('board.snakes outside bounds of self.board')
                if coord[1] < 0:
                    raise ValueError('board.snakes outside bounds of self.board')

    def to_dict(self):
        return {
            '_id': self.id,
            'game_id': self.game_id,
            'is_done': self.is_done,
            'turn': self.turn,
            'snakes': [snake.to_dict() for snake in self.snakes],
            'dead_snakes': [snake.to_dict() for snake in self.dead_snakes],
            'food': self.food[:],
            'width': self.width,
            'height': self.height,

            # TODO: Remove the need to have this here
            # Should push this into lib.game.engine.resolve_moves
            'board': self.generate_board(),
        }

    @classmethod
    def from_dict(cls, obj):
        game_state = cls(obj['game_id'], obj['width'], obj['height'])
        game_state.id = obj['_id']
        game_state.turn = obj['turn']
        game_state.is_done = obj['is_done']
        game_state.food = obj['food']

        from lib.game.engine import Snake
        game_state.snakes = [Snake.from_dict(snake) for snake in obj['snakes']]
        game_state.dead_snakes = [Snake.from_dict(snake) for snake in obj['dead_snakes']]

        game_state.sanity_check()

        return game_state
