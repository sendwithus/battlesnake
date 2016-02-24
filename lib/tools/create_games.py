import pymongo
from pymongo import MongoClient
from lib.game.engine import Engine, Snake
from lib.models.game import Game, GameState
from lib.models.team import Team

"""
   For performance testing I needed to generate games.
    I made some choices for efficiency as follows:

    * I chose to run 12 python-client (cloned from localsnakes) on my machine.
         * I needed clients that would survive reasonably long (not just move to the right)
         * I was not prepared to manage the creation of more clients
             - where would they run?
             - how many resources would they consome if I ran them locally?
             - starting/stoping them quicly would be a challenge.
    * I chose to use these same 12 clients in multiple, simultaneously running games
        * This was a short cut to get something running! and seems "good enough" :)

    So, this script grabs a list of teams and creates a game with them.

"""

# Game setup
width=30
height=30
turn_time=1
mode='advanced'

# NOTE: I attempted to use the Team object's find method. I can't choose the sort order
#       so I'm pulling teams out of mongo with pymongo
mongo = MongoClient()
db = mongo.battlesnake
team = db.team
MAX_NUM_TEAMS = 12

# get the first team 'Alfie'
admin = None

admin = team.find_one({'teamname': 'admin'})


team_dicts = team.find({}, {'teamname': True}).sort([('teamname', pymongo.ASCENDING)]).skip(0).limit(MAX_NUM_TEAMS)

teams = []
for team_dict in team_dicts:
    team = Team.find_one({'_id': team_dict['_id']})
    teams.append(team)
    print team.teamname, team.id, team.snake_url


# get the snake from the teams
snakes = [
    Snake(team_id=team.id, url=team.snake_url, name=team.teamname,
        # set thse all the same as i'm not querying the clients to get them -- they'll be the same anyway
        color="#000000",
        head="http://www.animated-gifs.eu/category_leisure/leisure-games-pacman/0009.gif",
        taunt="WAKAWAKAWAKAWAKAWAKA"
    )
    for team in teams
]

team_ids = [team.id for team in teams]

# Create a game and persis it
game = Game(width=width, height=height, turn_time=turn_time, mode=mode, team_id=admin['_id'], team_ids=team_ids)
game.insert()


# Create the first GameState
game_state = Engine.create_game_state(game.id, game.width, game.height, game.mode)

Engine.add_random_snakes_to_board(game_state, snakes)
Engine.add_starting_food_to_board(game_state)

# notify snakes that we're about to start
# notifies, gets taunt....that's about it.
# NOTE: not doing this here
# _update_snakes(game_state.snakes, ai.start(game, game_state))

# persist the game state
game_state.insert()
print game
print game_state

"""
# update the teams adding the games to their geam_ids list.
# no longer done!
for team_dict in teams:
		team = Team.find_one({'_id': team_dict.id})
		team.game_ids += [game.id]
		team.save()
		print "team.game_ids: %s" % team.game_ids
"""

# add the game id (name) to reddis to queue the games for the workes.
game.mark_ready()
