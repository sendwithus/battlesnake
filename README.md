BattleSnake 2016
================

#### presented by [sendwithus](https://www.sendwithus.com)

BattleSnake is a programming competition held in Victoria BC.

Teams from local schools and tech companies write AI clients for the game BattleSnake.

Last snake standing wins, prizes will be awarded to the most successful teams.

For more information or to register a team, visit [battlesnake.io](http://www.battlesnake.io).

__Questions?__ Email [battlesnake@sendwithus.com](mailto:battlesnake@sendwithus.com).

__Running BattleSnake game server__

This will walk you through setting up a game server instance. You probably don't need to do this unless you're helping improve BattleSnake for others.

1. [Install Vagrant](https://docs.vagrantup.com/v2/installation/index.html) if you don't already have it on your machine. We use vagrant to set up Mongo and Redis in a virtual machine without making a mess on your machine.

2. Once installed, in the root of the directory, run the following command. It will take a few minutes to complete so you can work on the next few python steps in the meantime.      

        $ vagrant up   

3. We'll use pip and virtualenv to run the python game server on your machine directly. pip is distributed with all modern versions of python but you may need to [install virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html) yourself.

4. Once installed, in the root of the directory, run the following commands. This will create a virtual environment locally and turn it on.

        $ virtualenv env --no-site-packages
        $ source env/bin/activate

5. Install the python libraries needed for the server. You may occasionally need to run this again if you run into an error complaining about a missing library.

        $ pip install -r requirements.txt

	Note: If you get an error that looks like `error: command 'cc' failed with exit status 1` when pip tries to install gevent, try running this instead:

        $ CFLAGS='-std=c99' pip install -r requirements.txt

6. The frontend uses node and react. If you don't have node V4 or above, you'll need to update your copy. First [install nvm](https://github.com/creationix/nvm). With nvm installed, run `nvm install` inside the project folder to use the right version of this project (defined in .nvmrc). You'll need to `nvm use` to activate the right version then run `npm install` (the node package manager) to install all of the required libraries.

7. We use foreman to run the game server. To install, you'll use Ruby's `gem`:

        $ sudo gem install foreman

8. With foreman installed, the python environment set up, and the vagrant VM setup finished, we're ready to run this shit!

        $ bin/run

9. If you get some messages about workers and pids, and nothing looks like an error, switch to your browser and visit [http://localhost:5000/](http://localhost:5000/).

You should be all set. To leave the project run:

    $ deactivate
    $ vagrant status

And to later re-enter the project, run:

    $ source env/bin/activate
    $ nvm use
    $ vagrant resume
    $ bin/run

__Admin accounts__

Only the 'admin' team can make certain changes such as registering teams. The first time you run the server, you'll need to create an admin account which can be done by running `bin/admin` or `heroku run bin/admin` in production.

__Managing database__

Occasionally, you may need to blow away the MongoDB database or something. Hopefully not in production.

    $ vagrant ssh
    [Connects to VM]
    $ mongo
    MongoDB shell version: 3.0.8
    connecting to: test
    > use battlesnake
    > show collections
    system.indexes
    team
    user
    > db.team.find()
    > db.team.remove({})
    > db.dropDatabase()
    > exit

__2015 Source Code__
* [github.com/sendwithus/battlesnake-legacy](http://github.com/sendwithus/battlesnake-legacy)

__2015 Starter Snakes__
* [NodeJS](http://github.com/sendwithus/battlesnake-node)
* [Python](http://github.com/sendwithus/battlesnake-python)
* [Java](http://github.com/sendwithus/battlesnake-java)
* [Ruby](http://github.com/sendwithus/battlesnake-ruby)
* [Go](http://github.com/sendwithus/battlesnake-go)
* [Clojure](https://github.com/sendwithus/battlesnake-clojure)
