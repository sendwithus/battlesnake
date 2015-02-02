import time

from pymongo import MongoClient

from lib.game import GameState
client = MongoClient('mongodb://EXulounJNLEl:qMwcAdTnxbnb@mongosoup-cont002.mongosoup.de:31615/cc_EXulounJNLEl')
db = client['battlesnake']


def run_game(game):
    print 'Running game %s' % game


def check_for_games():
    games = db.games.find({'status': 'waiting'}).sort('-created').limit(1)
    if games.count():
        run_game(games[0])
        return True
    else:
        print 'No Games'
        return False


def main():
    while True:
        check_for_games()
        time.sleep(1)

if __name__ == "__main__":
    main()
