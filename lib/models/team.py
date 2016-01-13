from werkzeug.security import generate_password_hash, check_password_hash
from lib.models.base import Model

import logging
logger = logging.getLogger(__name__)


class Team(Model):

    def __init__(self, teamname=None, password='', snake_url=None, member_emails=None, game_ids=None, is_public=False):
        super(Team, self).__init__()

        if member_emails is None:
            member_emails = []

        if game_ids is None:
            game_ids = []

        self.teamname = teamname
        self.set_password(password)
        self.snake_url = snake_url
        self.member_emails = member_emails
        self.game_ids = game_ids
        self.is_public = is_public

    # Flask-Login interface method
    def is_active(self):
        return True

    # Flask-Login interface method
    def get_id(self):
        return self.teamname

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
            'teamname': self.teamname,
            'pw_hash': self.pw_hash,
            'snake_url': self.snake_url,
            'member_emails': self.member_emails,
            'game_ids': self.game_ids,
            'is_public': self.is_public,
        }

    def serialize(self):
        return {
            'teamname': self.teamname,
            'snake_url': self.snake_url,
            'member_emails': self.member_emails,
            'game_ids': self.game_ids,
            'is_public': self.is_public,
        }

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
        return instance

    def ready_to_play(self):
        return self.snake_url is not None
