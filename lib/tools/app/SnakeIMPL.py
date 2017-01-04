from lib.tools.api.SnakeAPI import SnakeAPI
import json


class SimpleSnake(SnakeAPI):

    def whois(self):
        """ Responds: name, color, head """
        return {
                    'color': '#00ff00',
                    'head': 'HEAD_URL',
                    'name': 'hoo-ha!',
                }

    def start(self, payload):
        """ Responds: taunt """
        return {
            'taunt': "hoo-ha!"
        }

    def move(self, payload):
        """ Responds: move, taunt """
        print json.dumps(payload)
        return {
            'move': 'north',
            'taunt': 'battlesnake-python bitches!'
        }

    def end(self, payload):
        """ Responds: ignored """
        return {}
