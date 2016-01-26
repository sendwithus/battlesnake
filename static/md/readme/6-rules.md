## Game Rules

#### Objective

BattleSnake is an adaptation of the classic video game "Snake". Snake AIs control a snake as it moves around the game board interacting with food, walls, and other snakes. Each round may contain up to 8 snakes and the last snake alive wins the round.


#### Snakes will be killed if they...

* collide with the wall surrounding the game board
* collide with their own body
* collide with another snake**
* reach 0 health and starve (see below)

\*\*Head to head collisions result in the death of the shorter snake (or both if equal length).


#### Starvation

Snakes must eat regularly to survive. Your snake starts the game with 100 health points and loses 1 point each turn of game. If a snake reaches 0 health it will die of starvation.

To avoid starving to death you must ensure that your snake is well fed.

Food will spawn randomly throughout the board during the game. If your snake collides with the food it will consume it. Consuming food will return your snake to full health (100 health points). In addition to avoiding starvation, your snake will grow longer for every piece of food eaten.
