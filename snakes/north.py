from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'name': 'North Snake',
            'color': '#FFFFFF',
            'head': 'wut'
        }

    def start(self, payload):
        return {
            'taunt': 'northward bound'
        }

    def move(self, payload):
        return {
            'move': 'north',
            'taunt': 'still going north'
        }

    def end(self, payload):
        return {
            'taunt': 'oh no I died'
        }
