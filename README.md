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

6. We use foreman to actually run the server. It's bundled with the Heroku command line tools so you can [install those](https://devcenter.heroku.com/articles/heroku-command) or you can run `$ sudo gem install foreman`.

7. With foreman installed, the python environment set up, and the vagrant VM setup finished, we're ready to run this shit!

        $ bin/run

8. If you get some messages about workers and pids, and nothing looks like an error, switch to your browser and visit [http://localhost:5000/](http://localhost:5000/).

You should be all set. To leave the project run:

    $ deactivate
    $ vagrant status

And to later re-enter the project, run:

    $ source env/bin/activate
    $ vagrant resume
    $ bin/run

__2015 Source Code__
* [github.com/sendwithus/battlesnake-legacy](http://github.com/sendwithus/battlesnake-legacy)

__2015 Starter Snakes__
* [NodeJS](http://github.com/sendwithus/battlesnake-node)
* [Python](http://github.com/sendwithus/battlesnake-python)
* [Java](http://github.com/sendwithus/battlesnake-java)
* [Ruby](http://github.com/sendwithus/battlesnake-ruby)
* [Go](http://github.com/sendwithus/battlesnake-go)
* [Clojure](https://github.com/sendwithus/battlesnake-clojure)
