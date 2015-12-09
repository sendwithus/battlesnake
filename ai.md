# BattleSnake 2016 - AI Documentation

### GET /

TODO

##### Parameters
None

##### Response
* **name** - Friendly name of your snake
* **color** - CSS color for your snake's body
* **head** - Full URL to a 20x20 image for your snake's head

```json
{
    "name": "Snakebutt",
    "color": "#000000",
    "head": "http://your.domain/snake.jpg"
}
```


### POST /start

TODO

##### Parameters
* **game** - ID of game being started
* **mode** - Game mode, either `classic` or `advanced`
* **board** - Description of game board
  * **height** - Height of game board
  * **width** - Width of game board
* **snakes** - List of snakes included in this game

```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        {
            "name": "Taken Snake",
        }, ...
    ]
}
```

##### Response
* **taunt** - String message for other snakes

```json
{
    "taunt": "Let's rock!"
}
```


### POST /move

TODO

##### Parameters
* **game** - ID of game being played
* **mode** - Game mode, either `classic` or `advanced`
* **turn** - Turn number for this move
* **snakes** - List of snakes, including their status and position
* **board** - Description of current board state

```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "snakes": [ <Snake>, <Snake>, ... ],
    "board": [ <Board>, <Board>, ... ]
}
```

##### Response
* **move** - Direction of your next move, must be one of `["north", "south", "east", "west"]`
* **taunt** - String message for other snakes

```json
{
   "move": "north",
   "taunt": "To the north pole!!"
}
```

### POST /end

TODO

##### Parameters
* **game** - ID of game being played
* **mode** - Game mode, either `classic` or `advanced`
* **snakes** - List of snakes, including their final status and position
 
```json
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "snakes": [ <Snake>, <Snake>, ... ]
}
```

##### Response
* **taunt** - Final message to other snakes

```json
{
    "taunt": "gg, well played"
}
```

### Snake Objects

```json
```
