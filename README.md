# BattleSnake 2015
#### presented by [sendwithus](https://www.sendwithus.com), powered by [Heroku](http://heroku.com)

BattleSnake is a programming competition held in Victoria BC.

Teams from local schools and tech companies write AI clients for the game BattleSnake.

Last snake standing wins, prizes will be awarded to the most successful teams.

API details and documentation will be released and discussed the morning of the event.

For more information or to register a team, visit [battlesnake.io](http://www.battlesnake.io).

__Questions?__ Email [battlesnake@sendwithus.com](mailto:battlesnake@sendwithus.com). 

<br>

#### Table of Contents
* [Location and Schedule](#location-and-schedule)
* [Preparing for Battle](#preparing-for-battle)
* [Prizes and Awards](#prizes-and-awards)
* [Game Rules](#game-rules)
* [Snake API Documentation](#snake-api-documentation)
* [Example Snakes](#example-snakes)
* [Testing Snakes](#testing-snakes)

<br>

#### BattleSnake is Sponsored By
* [Heroku](http://www.heroku.com)
* [sendwithus](http://www.sendwithus.com)
* [Dropbox](http://www.dropbox.com)
* [VIATeC](http://www.viatec.ca)
* [OneNet Marketing](http://onenetmarketing.com)
* [University of Victoria, Department of Computer Science](https://www.csc.uvic.ca/)
* [University of Victoria, Technology Integrated Learning](http://www.uvic.ca/til/)
* [Women in Engineering and Computer Science (WECS)](https://wecs.csc.uvic.ca/)
* [UVic Computer Science Course Union (CSCU)](https://onlineacademiccommunity.uvic.ca/cscu/)
* [UVic Web Development Club](http://uvic.io/)

<br>

## Location and Schedule

__When__ <br> February 21st, 11:00am - 8:00pm

__Where__ <br> University of Victoria, ECS 123 ([map](https://www.google.ca/maps/place/Engineering+Laboratory+Wing,+University+of+Victoria,+Victoria,+BC+V8P+3E6/@48.4610471,-123.3105421,17z/data=!3m1!4b1!4m6!1m3!3m2!1s0x0:0xc039d0b85e1ede74!2sUniversity+of+Victoria!3m1!1s0x548f71564531ee1b:0xa0671c6aceab37b4))

__Schedule__

| Time | Event |
|----------|--------|
| 11:00am | Team Registation |
| 11:30am | Orientation and Game Rules |
| 12:00pm | Hacking Begins! |
| 12:30pm | Food |
| 5:30pm | More Food! |
| 6:00pm | BattleSnake Tournament Starts |
| 7:30pm | Drinks @ Felicita's |


<br>

## Preparing for Battle
Everything you need to know before attending BattleSnake.

### Come Prepared

Your team __will be writing code__, come prepared to do so. You should also have the following ready
* Laptop with the following setup:
  * Git
  * Programming language of choice (Node, Python, Java, etc)
  * A text editor (Sublime Text, Vim, etc)
* A [GitHub](http://github.com) account
* A free [Heroku](http://heroku.com) account

### Learning Heroku

For novice and intermediate programmers, we __strongly__ recommend familiarizing yourself with [Heroku](http://heroku.com) before hand. Deploying with [Heroku](http://heroku.com) will maximize time spent developing your AI (and not messing around with servers). All provided code samples and example AIs will be ready-to-deploy to Heroku.

Also see
* [Getting Started on Heroku](https://devcenter.heroku.com/start)
* [Heroku Toolbelt](https://toolbelt.heroku.com/)
* [Deploying to Heroku with Git](https://devcenter.heroku.com/articles/git)
* [Deploying to Heroku with Dropbox](https://devcenter.heroku.com/articles/dropbox-sync)

### Registration

Team registration opens at 11:00am in ECS 123.

To register, you'll need the following:
* Team/Snake Name
* Name of all team members (1-4 suggested)

Individuals may register and compete as a one person team. Anyone looking to join a team will be accommodated.

### Orientation

Orientation will start __promptly__ at 11:30am. __Do not be late.__

Topics covered during orientaion
* Tournament format and schedule
* Game rules and API documentation
* Sample code for Python, Node, Java, Ruby, and Go
* Where to find help

Orientation will also be the best time to ask questions. Hacking will start immediately afterwards.

<br>

## Prizes and Awards

#### Grand Prize 
$500 Cash, Swag Pack

#### Second Place
$300 Cash, Swag Pack

#### Third Place
$200, Swag Pack

#### Heroku Award 
Heroku Longboard [Register Here](http://heroku.getfeedback.com/battlesnake)

#### Dropbox Award
1TB Dropbox Space [Register Here](http://bit.ly/dropbox-battlesnake)

__Swag Pack Awards__
* Hunger Games Snake (most food eaten)
* Predator Snake (most kills)
* Never Surrender Snake (longest)

<br>

## Game Rules

This is how things work.

### Objective

BattleSnake is an adaptation of the classic video game "Snake" where you control a snake as it move around the play field.  Each round pits up to X snakes against eachother, and the goal is to be the last snake left alive at the end of the round.

### How do you die?

* Running into another snake.
* Running into your own body.
* Running into the walls of the play field.
* Head to head collisions result in the death of the shorter snake (or both if tied).
* Your snake starves.

### Starvation

* It's a snake eat snake world out there, and you must eat regularly to survive.
* Your snake starts out with 100 life, and counts down by 1 each turn.
* When your life total reaches 0, your snake dies of starvation.

### How to avoid starvation?

* To avoid being sacrificed, you must ensure that your snake is well fed.
* Food will spawn randomly around the board.
* Each piece of food eaten will increase the length of your snake by 1, and reset your life to 100.
* Killing another snake by cutting them off with your body will increase the length of your own snake and reset your life to 100.
* Kills increase your length by half of the victims length, rounded down.

### Sportsmanship

* Fuck sportmanship.

<br>

## Snake API Documentation

For more information visit [battlesnake.io](http://www.battlesnake.io).

### General Client Rules

* Game clients must exist at a valid HTTP URL capable of responding to the requests specified below.
* Clients must respond to all requests within 2 seconds or face disqualification.
* All requests must return a 200 status code and a valid response body or face disqualification.

### POST /start

Signals the start of a BattleSnake game. All clients must respond with a 200 status code and valid response object or risk being disqualified.

Since game IDs may be re-used, this endpoint may be called multiple times with the same game ID. Clients use this call to reset any saved game state for the given game ID.

##### Request

* **game_id** - ID of the game about to start
* **width** - The width of the game board (the x axis)
* **height** - The height of the game board (the y axis)

```javascript
{
  "game_id": "hairy-cheese",
  "width": 20,
  "height": 20
}
```

##### Response

* **name** - friendly name of this snake
* **color** - display color for this snake (must be CSS compatible)
* **head_url** _(optional)_ - full URL for a 100x100 snake head image
* **taunt** _(optional)_ - string message for other snakes

```js
{
  "name": "Team Gregio",
  "color": "#ff0000",
  "head_url": "http://img.server.com/snake_head.png",
  "taunt": "Let's rock!"
}
```

### POST /move

Failing to respond appropriately
if invalid response, snake moves forward

##### Request

* **game_id** - ID of the game being played
* **turn** - turn number being played
* **board** - current board state (see [Board State Objects](#board-state-objects))
* **snakes** - array of snakes in play (see [Snake Objects](#snake-objects))
* **food** - array of food coordinates (see [Food Arrays](#food-arrays))

```javascript
{
  "game_id": "hairy-cheese",
  "turn": 1,
  "board": [
    [<BoardTile>, <BoardTile>, ...],
    [<BoardTile>, <BoardTile>, ...],
    ...
  ],
  "snakes":[<Snake>, <Snake>, ...],
  "food": [[1, 4], [3, 0], [5, 2]]
}
```

##### Response

* **move** - this snakes' next move, one of: ["up", "down", "left", "right"]
* **taunt** _(optional)_ - string message to other snakes

```javascript
{
  "move": "up",
  "taunt": "go snake yourself"
}
```

### POST /end

Indicates that a specific game has ended. No more move requests will be made. No response required.

##### Request

* **game_id** - id of game being ended

```javascript
{
  "game_id": "hairy-cheese"
}
```

##### Response

_Responses to this endpoint will be ignored._

### Board State Objects

Describes the state of the board for a specific game. Board State Objects are comprised of a 2-Dimensional array of Board Tiles. This array is indexed to match board coordinates, such that the board tile for coordinates (1, 5) are accessible at _board[1][5]_. Board coordinates are 0-based with [0][0] representing the top left corner.

![board.jpg](/static/img/board.jpg)

##### Example Board State

```javascript
[
  [<BoardTile>, <BoardTile>, ...],
  [<BoardTile>, <BoardTile>, ...],
  ...
]
```

##### Board Tiles

* **state** - one of ["head", "body", "food", "empty"]
  * _head_ - occupied by snake head (see snake attribute)
  * _body_ - occupied by snake body (see snake attribute)
  * _food_ - contains an uneaten piece of food
  * _empty_ - an empty tile
* **snake** _(optional)_ - name of occupying snake (if applicable)

```javascript
{
  "state": "head",
  "snake": "Noodlez"
}
```

### Snake Objects

Describes the state of a single snake in a particular game.

##### Attributes

* **name** - friendly name of this snake (must be unique)
* **state** - snake state, one of ["alive", "dead"]
* **coords** - ordered array of coordinates indicating location of this snake on the board (from head to tail)
* **score** - current score
* **color** - display color for this snake
* **head_url** - full URL to 20x20 snake head image
* **taunt** - latest string message to other snakes

```javascript
{
  "name": "Noodlez",
  "state": "alive",
  "coords": [[0, 0], [0, 1], [0, 2], [1, 2]],
  "score": 4,
  "color": "#ff0000",
  "head_url": "http://img.server.com/snake_head.png",
  "taunt": "I'm one slippery noodle"
}
```

### Food Arrays

An array of coordinate tuples representing food locations.

##### Example

```javascript
[
  [1, 4], [3, 0], [5, 2]
]
```

<br>

## Example Snakes

The sendwithus team has provided basic Snake AIs to get you started. Each of these clients can be deployed to [Heroku](http://heroku.com) without additional configuration.

__Starter Snakes__
* [NodeJS](http://github.com/sendwithus/battlesnake-node)
* [Python](http://github.com/sendwithus/battlesnake-python)
* [Java](http://github.com/sendwithus/battlesnake-java)
* [Ruby](http://github.com/sendwithus/battlesnake-ruby)
* [Go](http://github.com/sendwithus/battlesnake-go)
* [Clojure](https://github.com/sendwithus/battlesnake-clojure)

__Example Snakes (that work, but suck)__
* Solid BattleSnake - [http://battlesnake-dylan.herokuapp.com](http://battlesnake-dylan.herokuapp.com)
* Liam Neeson - [http://battlesnake-greedy.herokuapp.com](http://battlesnake-greedy.herokuapp.com)
* Trouser Basilisk - [http://battlesnake-will.herokuapp.com](http://battlesnake-will.herokuapp.com)
* faroutsnake - [http://mattsnake.herokuapp.com/](http://mattsnake.herokuapp.com)
* Swift Snake - [http://battlesnake-jer2.herokuapp.com](http://battlesnake-jer2.herokuapp.com)
* Randosnake - [http://battlesnake-rando.herokuapp.com](http://battlesnake-rando.herokuapp.com)
* Coward Snake - [battlesnake-coward.herokuapp.com](http://battlesnake-coward.herokuapp.com)

<br>

## Testing Snakes

* Mention ngrok.
* Mention debug mode.
* Mention papertrail.

<br>

## Questions?

Email [battlesnake@sendwithus.com](mailto:battlesnake@sendwithus.com).

For more information or to register a team, visit [battlesnake.io](http://www.battlesnake.io).
