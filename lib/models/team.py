import logging
import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from lib.models.base import Model
from lib.models.game import Game

logger = logging.getLogger(__name__)


class Team(Model):
    TYPE_NORMAL = 'normal' # Standard contestant snake, only type allowed in tournament
    TYPE_ADMIN  = 'admin'  # Is an super user team (doesn't appear in the UI at all)
    TYPE_BOUNTY = 'bounty' # Bounty snake from a sponsor
    TYPE_TEST   = 'test'   # Snake to test against
    TYPE_VALUES = [TYPE_NORMAL, TYPE_ADMIN, TYPE_BOUNTY, TYPE_TEST]

    def __init__(
            self,
            id=None,
            teamname=None,
            password='',
            snake_url=None,
            member_emails=None,
            game_ids=None,
            game_mode=Game.MODE_CLASSIC,
            is_public=False,
            type=TYPE_NORMAL):

        super(Team, self).__init__()

        # Set Defaults

        if member_emails is None:
            member_emails = []

        if game_ids is None:
            game_ids = []

        if id is None:
            id = Team._generate_id()

        # Define Properties

        self.id = id
        self.teamname = teamname
        self.pw_hash = None
        self.snake_url = snake_url
        self.member_emails = member_emails
        self.game_ids = game_ids
        self.is_public = is_public
        self.game_mode = game_mode
        self.type = type

        # Other things

        self.set_password(password)

    # Override save to enforce some things
    def save(self):
        # Remove trailing slashes from Snake URLS
        if self.snake_url:
            self.snake_url = self.snake_url.rstrip("/")

        super(Team, self).save()

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())

    # Flask-Login interface method
    def is_active(self):
        return True

    # Flask-Login interface method
    def get_id(self):
        return self.id

    # Flask-Login interface method
    def is_authenticated(self):
        return True

    # Flask-Login interface method
    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def to_dict(self):
        return {
            '_id': self.id,
            'teamname': self.teamname,
            'pw_hash': self.pw_hash,
            'snake_url': self.snake_url,
            'member_emails': self.member_emails,
            'game_ids': self.game_ids,
            'game_mode': self.game_mode,
            'is_public': self.is_public,
            'type': self.type,
        }

    def serialize(self):
        d = self.to_dict()
        del d['pw_hash']
        return d

    @classmethod
    def from_dict(cls, obj):
        instance = cls(
            teamname=obj['teamname'],
            snake_url=obj.get('snake_url', None),
            member_emails=obj.get('member_emails', []),
        )
        instance.id = obj['_id']
        instance.pw_hash = obj['pw_hash']
        instance.game_ids = obj['game_ids']
        instance.is_public = obj['is_public']
        instance.game_mode = obj.get('game_mode', Game.MODE_CLASSIC)

        legacy_type = Team.TYPE_BOUNTY if obj.get('is_bounty', False) else Team.TYPE_NORMAL
        instance.type = obj.get('type', legacy_type)
        # NOTE: Using dict.get() on some of these so we don't have to do migrations

        return instance

    def ready_to_play(self):
        return self.snake_url is not None
