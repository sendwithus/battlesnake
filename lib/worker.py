from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['battlesnake']

games = db['games']
game_states = db['game_states']


class (object):
