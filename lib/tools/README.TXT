
I put this together quickly from something else I wrote.

   * I use the exiting local snakes and modified them to accept their 'team id' from the environment.
     see game-clients-start.sh.
  * Given limited resources, the script to create games always uses the same 12 teams: the first 12 from an alpha sort
    I chose to do this.
  * I startup 12 python clients snakes and these will play multiple games simultaneously.
    Remember, my objective was to simulate game play on the server and test performance.

Usage:

   1) run create_teams.py (once) to create 303 teams: teams are uniquely named using names from the names.txt file.
   2) run games_start.sh (as many times as you want) to create 'number_of_games' games. number_of_games = 64.
   3) run "games-clients-start.sh start" (once) [and games-clients-start.sh stop] to start the 12 python-client games.
          Note: passing stop will kill the processes for you.


Files:

names.txt
    a list of dog names.  Feel free to use some other list.  The names are used to created the team name and their email, so no spaces in the names please.

create_teams.py
    This imports modules from battlesnake and automates the creation on 303 teams -- the number of names in the names.txt.

create_games.py
    This imports modules from battlesnake and automates the creation of games.
    Note: run games_start.sh as it calls this script.
    It creates one game with 12 (the first 12 teams in alphabetical order, that were created with create_teams.py)
      * 30X30 matrix
      * advanced mode.
      * created by the admin user -- so be sure to launch admin game workers.
      * 12 snakes per game

game-client-start.sh
    This launches 12 cloned python-client snakes.
    It's not fancy, the snakes are not the greatest...they're pretty good.  When I wrote this only Curtis's localsnake played reasonably well.

games_start.sh
    This is a script that creates number_of_games games using create_games.py.


Other Notes:
  I used Dex (https://github.com/mongolab/dex) to find missing indexes in MongoDB in the VM - the drastically reduced CPU usage.
  The services directory contains installation crib notes and configs for a number of services I installed in my VM that I found useful:
    battlesnake: I installed the system in the VM as I was intending to do some instrumentation and performance analytics gathering
      meh.  it was useful just the same to have it running in the VM as I can then run top and see whether it was a heavy hitter or not.
    mongo-express:  this was a great simple web-app I used to poke around the mongoDB collections.   I found that we were storing the board
           state which was unnecessary and a large waste of space. :)
    redis-commander:  Another web-app I used to poke around redis.  After games are created, the gameid is put into a list in redis
           which the workers then consume and run. That's it.
    grafana:  This is in fact a collection of services:
        collectd: to collect metrics
        collectd-mongodb: a plugin for collectd that gather's metrics on mongodb
        influxDB: This is an open source distributed time series database.  I collect data from collectd.
        grafana:  A tool for using misc data stores of time series data and creating and presenting cool dashboard.
                  I use this to figure out that mongodb was going bonkers consuming CPU.

   To get all these working will require a little bit of configuration.  I've decided not to add it to the Vagrant file, but put everything here
   in crib notes instead.

   I had to increment the amount of memory in the VM to 2GiB - just to get node to compile battlesnake, then I incremented to 4026 to try and get
   better performance. -- it was the missing indexes in mongodb that were the problem :)

   Here are the port configurations I had in my Vagrant file.

        config.vm.network "forwarded_port", guest: 1234,  host: 1234  # adminMongo
        config.vm.network "forwarded_port", guest: 8081,  host: 8081  # mongo-express
        config.vm.network "forwarded_port", guest: 8082,  host: 8082  # redis-commander
        config.vm.network "forwarded_port", guest: 4474,  host: 4474  # livereact
        config.vm.network "forwarded_port", guest: 8083,  host: 8083  # InfluxDB GUI
        config.vm.network "forwarded_port", guest: 8086,  host: 8086  # InfluxDB
        config.vm.network "forwarded_port", guest: 3000,  host: 3000  # Grafana

   The Indexes I added were:

   sudo mongo battlesnake --eval 'db["team"].ensureIndex({"teamname": 1}, {"background": true})'
   sudo mongo battlesnake --eval 'db["gamestate"].ensureIndex({"game_id": 1, "created": 1}, {"background": true})'

   NOTE: there may be other indexes to be added.   I did not simulate multiple web clients viewing game play.
   If we were thorough we would examine the query plan of every query being executed.
