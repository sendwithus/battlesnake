import logging

from lib.models.base import Model

logger = logging.getLogger(__name__)


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
