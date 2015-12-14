import logging

from lib.models.base import Model
from lib.words import get_noun, get_adjective


logger = logging.getLogger(__name__)


class Team(Model):

    def __init__(
            self,
            id=None,
            snake_url=None,
            member_emails=[]):

        super(Team, self).__init__()

        self.id = id or Team._generate_id()
        self.snake_url = snake_url
        self.member_emails = member_emails

    def to_dict(self):
        return {
            '_id': self.id,
            'snake_url': self.snake_url,
            'member_emails': self.member_emails,
        }

    @staticmethod
    def _generate_id():
        return 'team-%s-%s' % (get_adjective(), get_noun())

    @classmethod
    def from_dict(cls, obj):
        instance = cls(
            id=obj['_id'],
            snake_url=obj['snake_url'],
            member_emails=obj['member_emails'],
        )

        instance._add_timestamps(obj)
        return instance
