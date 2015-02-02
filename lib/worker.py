import time

from pymongo import MongoClient

from lib.game import GameState
client = MongoClient(os.environ['MONGOLAB_URI'])
db = client.get_default_database()


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
