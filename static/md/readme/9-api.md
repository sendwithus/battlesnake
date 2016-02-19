## BattleSnake API Documentation

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

---

### INFO <br> _GET /_

Returns information about your snake.

Visiting your snake URL in a browser should return this information, which is a good way to make sure your server is working as expected. This command may also be called by the BattleSnake game servers at any point during or outside a game.

#### Request Parameters

None

#### Response

* **color** - CSS color for your snake's body
* **head** - Full URL to a 20x20 image for your snake's head

```json
{
    "color": "#FF0000",
    "head": "http://www.clker.com/cliparts/D/i/A/w/J/R/snake-no-white-drule-hi.png",
}
```

<hr>

### START GAME <br> _POST /start_

Signals the start of a BattleSnake game.

NOTE: Game IDs may be re-used throughout the day, however multiple games with the same ID will not be running at the same time. It's your snake's responsibility to clear any saved data for a previous game with the same game ID.

#### Request Parameters

* **game** - ID of game being played
* **mode** - Game mode, either _"classic"_ or _"advanced"_
* **turn** - Turn number for this move
* **height** - Height of game board
* **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food
* **walls** - List of coordinates of extra walls (Advanced Only)
* **gold** - Coordinates of available gold coins (Advanced Only)

```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 0,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        &lt;Snake Object&gt;, &lt;Snake Object&gt;, ...
    ],
    "food": [],
    "walls": [],  // Advanced Only
    "gold": []    // Advanced Only
}
```

#### Response

* **taunt** - String message for other snakes

```json
{
    "taunt": "Let's rock!"
}
```

---

### MOVE <br> _POST /move_

Request for your snake to move. This request is made to all snakes in a particular game simultaneously. Once all snakes have responded, moves are calculated and the game board will update.

NOTE: Failing to properly respond to a MOVE command will forfeit your turn and your snake will move forward regardless of what lies ahead. Repeated failures may disqualify your snake from the game.

#### Request Parameters

* **game** - ID of game being played
* **mode** - Game mode, either _"classic"_ or _"advanced"_
* **turn** - Turn number for this move
* **height** - Height of game board
* **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food
* **walls** - List of coordinates of extra walls (Advanced Only)
* **gold** - Coordinates of available gold coins (Advanced Only)


```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        &lt;Snake Object&gt;, &lt;Snake Object&gt;, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}
```

#### Response

* **move** - Direction of your next move, must be one of _["north", "south", "east", "west"]_
* **taunt** - String message for other snakes

```json
{
   "move": "north",
   "taunt": "To the north pole!!"
}
```

---

### END GAME <br> _POST /end_

Signals the end of a specific game. After this request, future requests for this Game will not be made and the Game ID may be re-used.

#### Parameters

* **game** - ID of game being played
* **mode** - Game mode, either _"classic"_ or _"advanced"_
* **turn** - Turn number for this move
* **height** - Height of game board
* **width** - Width of game board
* **snakes** - List of snakes, including their status and position
* **food** - List of coordinates of available food
* **walls** - List of coordinates of extra walls (Advanced Only)
* **gold** - Coordinates of available gold coins (Advanced Only)

```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        &lt;Snake Object&gt;, &lt;Snake Object&gt;, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}
```

#### Response

Ignored, game is over.

```json
{}
```

---

### Snake Objects

Snake objects have the following properties:

* **id** - Snake ID. Use this value to find your snake [(find your ID here)](http://www.battlesnake.io/team).
* **name** - Snake Name
* **status** - Status, either _"alive"_ or _"dead"_
* **message** - Friendly message describing this snakes last move
* **taunt** - Snake's latest taunt
* **age** - How many turns this snake has survived
* **health** - Current snake health [0 - 100]
* **coords** - List of [x, y] coordinates describing snake position, ordered from head to tail
* **kills** - Number of snake deaths this snake is responsible for
* **food** - Number of food eaten by this snake
* **gold** - Number of gold coins acquired by this snake

```json
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
    "food": 12,
    "gold": 2
}
```
