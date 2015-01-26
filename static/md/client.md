# [BattleSnake] Client API

## General Client Rules

*   Game clients must exist at a valid HTTP URL capable of responding to the requests specified below.
*   Clients must respond to all requests within 2 seconds or face disqualification.
*   All requests must return a 200 status code and a valid response body or face disqualification.

## POST /start

Signals the start of a BattleSnake game. All clients must respond with a 200 status code and valid response object or risk being disqualified.

Since game IDs may be re-used, this endpoint may be called multiple times with the same game ID. Clients use this call to reset any saved game state for the given game ID.
<undefined><li>**<u>Request</u>**</li></undefined>

*   **id** - ID of the game about to start

*   {
*       "id": "hairy-cheese"
*   }

<undefined><li>**<u>Response</u>**</li></undefined>

*   **name **-** **friendly name of this snake
*   **color **- display color for this snake (must be CSS compatible)
*   **head_url**_ (optional)_ - full URL for a 20x20 snake head image
*   **taunt**_ (optional)_ - string message for other snakes

*   {
*       "name": "Team Gregio",
*       "color": "#ff0000",
*       "head_url": "[](http://img.server.com/snake_head.png)http://img.server.com/snake_head.png",
*       "taunt": "Let's rock!"
*   }

## POST /move

Failing to respond appropriately

if invalid response, snake moves forward
<undefined><li>**<u>Request</u>**</li></undefined>

*   **id** - ID of the game being played
*   **turn** - turn number being played
*   **board** - current board state (see [Board State Objects](/Battle-Snake-Client-API-FaFoovzSb9v#:h=Board-State-Objects))
*   **snakes** - array of snakes in play (see [Snake Objects](/Battle-Snake-Client-API-FaFoovzSb9v#:h=Snake-Objects))

*   {
*       "id": "hairy-cheese",
*       "turn": 1,
*       "board": [
*           [<BoardTile>, <BoardTile>, ...],
*           [<BoardTile>, <BoardTile>, ...],
*           ...
*       ],
*       "snakes":[<Snake>, <Snake>, ...]
*   }

<undefined><li>**<u>Response</u>**</li></undefined>

*   **move** - this snakes' next move, one of: ["up", "down", "left", "right"]
*   **taunt** _(optional)_ - string message to other snakes

*   {
*       "move": "up",
*       "taunt": "go snake yourself"
*   }

## POST /end

Indicates that a specific game has ended. No more move requests will be made. No response required.
<undefined><li>**<u>Request</u>**</li></undefined>

*   **id** - id of game being ended
*

*   {
*       "id": "hairy-cheese"
*   }

<undefined><li>**<u>Response</u>**</li></undefined>

*   _Responses to this endpoint will be ignored._

## Board State Objects

Describes the state of the board for a specific game. Board State Objects are comprised of a 2-Dimensional array of Board Tiles. This array is indexed to match board coordinates, such that the board tile for coordinates (1, 5) are accessible at _board[1][5]_. Board coordinates are 0-based.
<undefined><li>**<u>Example Board State</u>**</li></undefined>

*   [
*       [<BoardTile>, <BoardTile>, ...],
*       [<BoardTile>, <BoardTile>, ...],
*       ...
*   ]

<undefined><li>**<u>Board Tiles</u>**</li></undefined>
<ul style="list-style: none;"><li>**type** - one of ["head", "body", "food", "empty"]

*   _head_ - occupied by snake head (see snake attribute)
*   _body_ - occupied by snake body (see snake attribute)
*   _food_ - contains an uneaten piece of food
*   _empty_ - an empty tile
</ul style="list-style: none;">

*   **snake** (optional) - snake id of occupying snake (if applicable)

*   {
*       "type": "head",
*       "snake": "snake_19283"
*   }

## Snake Objects

Describes the state of a single snake in a particular game.
<undefined><li>**<u>Attributes</u>**</li></undefined>

*   **id** - unique id for this snake in the current game
*   **name** - friendly name of this snake
*   **state** - snake state, one of ["alive", "dead"]
*   **coords** - ordered array of coordinates indicating location of this snake on the board (from head to tail)
*   **score** - current score
*   **color** - display color for this snake
*   **head_url** - full URL to 20x20 snake head image
*   **taunt** - latest string message to other snakes

*   {
*       "id": "snake_19283",
*       "name": "Noodlez",
*       "state": "alive",
*       "coords": [[0, 0], [0, 1], [0, 2], [1, 2]],
*       "score": 4,
*       "color": "#ff0000",
*       "head_url": "[](http://img.server.com/snake_head.png)[http://img.server.com/snake_head.png](http://img.server.com/snake_head.png)",
*       "taunt": "I'm one slippery noodle"
*   }