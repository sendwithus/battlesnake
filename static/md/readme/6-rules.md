## Classic Game Rules

### Objective

BattleSnake is an adaptation of the classic arcade game "Snake". Teams build web servers to control a snake as it moves around the game board interacting with food, walls, and other snakes.

Each game may contain up to 12 snakes. The last snake alive wins the game.

### Snakes will die if they...

* reach 0 health and starve (see below)
* collide with the edges of the game board
* collide with their own body
* collide with another snake**

\*\*Head to head collisions result in the death of the shorter snake (or both if equal length).


### Starvation

Snakes must eat regularly to survive. Each snake starts the game with 100 health and loses 1 health each turn of the game. If a snake reaches 0 health it will die of starvation.

To avoid starving to death you must ensure that your snake is well fed.

Food will spawn throughout the board during the game. If your snake collides with the food it will consume it. Consuming food will add 30 health to your snake (up to 100 maximum). In addition to avoiding starvation, your snake will grow longer for every piece of food eaten.

Growing your snake can be helpful or make the game more challenging to win, depending on how your AI behaves.
