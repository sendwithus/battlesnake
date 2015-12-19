from lib.ai.local import LocalSnake


class Snake(LocalSnake):

    def whois(self):
        return {
            'name': 'BradSnake',
            'color': '#f0f087',
            'head': 'barf'
        }

    def start(self, payload):
        return {
            'taunt': 'go taunt yourself'
        }

    def move(self, payload):
        return {
            'move': 'north',
            'taunt': 'up up and away!'
        }

    def end(self, payload):
        return {
            'taunt': 'barf I died'
        }
