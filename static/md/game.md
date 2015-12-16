# BattleSnake Game Rules

*Work in progress.*

<br>

## Objective

BattleSnake is an adaptation of the classic video game "Snake" where you control a snake as it move around the play field.  Each round pits up to X snakes against eachother, and the goal is to be the last snake left alive at the end of the round.

## How do you die?

* Running into another snake.
* Running into your own body.
* Running into the walls of the play field.
* Head to head collisions result in the death of the shorter snake (or both if tied).
* Your snake starves.

## Starvation

* It's a snake eat snake world out there, and you must eat regularly to survive.
* Your snake starts out with 100 life, and counts down by 1 each turn.
* When your life total reaches 0, your snake dies of starvation.

## How to avoid starvation?

* To avoid being sacrificed, you must ensure that your snake is well fed.
* Food will spawn randomly around the board.
* Each piece of food eaten will increase the length of your snake by 1, and reset your life to 100.
* Killing another snake by cutting them off with your body will increase the length of your own snake and reset your life to 100.
* Kills increase your length by half of the victims length, rounded down.

## Sportsmanship

* There are no rules.
