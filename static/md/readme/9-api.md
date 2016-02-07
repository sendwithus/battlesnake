## Snake API Documentation

The BattleSnake API uses JSON formatted HTTP requests and responses. Snakes must reply to each command:

* within one second
* with a 200 HTTP Status Code
* with a properly formatted JSON response

Failure to meet any of these requirements may disqualify your snake from participating in a game.

#### Commands

The BattleSnake API consists of four commands:

* INFO
* START GAME
* MOVE
* END GAME

### COMMAND: INFO <br> _GET /_

Returns information about your snake.

Visiting your snake URL in a browser should return this information, which is a good way to make sure your server is working as expected. This command may also be called by the BattleSnake game servers at any point during or outside a game.

#### Request Parameters

None

#### Response

* **color** - CSS color for your snake's body
* **head** - Full URL to a 20x20 image for your snake's head

<code><pre>
{
    "color": "#FF0000",
    "head": "http://www.clker.com/cliparts/D/i/A/w/J/R/snake-no-white-drule-hi.png",
}
</code></pre>

### COMMAND: START GAME <br> _POST /start_

Signals the start of a BattleSnake game.

NOTE: Game IDs may be re-used throughout the day, however multiple games with the same ID will not be running at the same time. It's your snake's responsibility to clear any saved data for a previous game with the same game ID.

#### Request Parameters

* **game** - ID of game being played
* **mode** - Game mode, either `classic` or `advanced`
* **turn** - Turn number for this move
* **board**
    * **height** - Height of game board
    * **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food

<code><pre>
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 0,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        <Snake>, <Snake>, ...
    ],
    "food": []
}
</code></pre>

#### Response

* **taunt** - String message for other snakes

<code><pre>
{
    "taunt": "Let's rock!"
}
</code></pre>

### COMMAND: MOVE <br> _POST /move_

Request for your snake to move. This request is made to all snakes in a particular game simultaneously. Once all snakes have responded, moves are calculated and the game board will update.

NOTE: Failing to properly respond to a MOVE command will forfeit your turn and your snake will move forward regardless of what lies ahead. Repeated failures may disqualify your snake from the game.

#### Request Parameters

* **game** - ID of game being played
* **mode** - Game mode, either `classic` or `advanced`
* **turn** - Turn number for this move
* **board**
    * **height** - Height of game board
    * **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food

<code><pre>
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        <Snake>, <Snake>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ]
}
</code></pre>

#### Response

* **move** - Direction of your next move, must be one of `["north", "south", "east", "west"]`
* **taunt** - String message for other snakes

<code><pre>
{
   "move": "north",
   "taunt": "To the north pole!!"
}
</code></pre>

### COMMAND: END <br> _POST /end_

Signals the end of a specific game. After this request, future requests for this Game will not be made and the Game ID may be re-used.

#### Parameters

* **game** - ID of game being played
* **mode** - Game mode, either `classic` or `advanced`
* **turn** - Turn number for this move
* **board**
    * **height** - Height of game board
    * **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food

<code><pre>
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        <Snake>, <Snake>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ]
}
</code></pre>

#### Response

Ignored, game is over.

<code><pre>
{}
</code></pre>

### Snake Objects

Snake objects have the following properties:

* **id** - Snake ID. Use this value to find your snake, [find your ID here](http://www.battlesnake.io/team).
* **name** - Snake Name
* **status** - Status, either `alive` or `dead`
* **message** - Friendly message describing this snakes last move
* **taunt** - Snake's latest taunt
* **age** - How many turns this snake has survived
* **health** - Current snake health (0 - 100)
* **coords** - List of [x, y] coordinates describing snake position, ordered from head to tail
* **kills** - Number of snake deaths this snake is responsible for
* **food** - Number of food eaten by this snake

<code><pre>
{
    "id": "1234-567890-123456-7890",
    "name": "Well Documented Snake",
    "status": "alive",
    "message": "Moved north",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ],
    "kills": 4,
    "food": 12
}
</code></pre>
