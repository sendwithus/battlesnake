from werkzeug.security import generate_password_hash, check_password_hash
from lib.models.base import Model

import logging
logger = logging.getLogger(__name__)


class Team(Model):

    def __init__(self, teamname=None, password='', snake_url=None, member_emails=[]):
        super(Team, self).__init__()

        self.teamname = teamname
        self.set_password(password)
        self.snake_url = snake_url
        self.member_emails = member_emails

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
            'member_emails': self.member_emails
        }

    def serialize(self):
        return {
            'teamname': self.teamname,
            'snake_url': self.snake_url,
            'member_emails': self.member_emails
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
        return instance


# Always recreate a default team for testing
Team._get_collection().remove({'teamname': 'default'})
default_team = Team('default', 'nopassword')
default_team.insert()
