![Sendwithus Logo](content/swu-logo.svg)

...
- Introduce ourselves.

---

![Battlesnake Logo](content/battlesnake-logo.svg) <!-- .element: width="95%" -->

---

## Everything you need
<br/>
### battlesnake.io
### battlesnake.io/docs

...
Everything you will need to know will be available at these URLs

---

## What is Battlesnake?

AI competition held annually, on its 4th year

As a competitor, _you_ code the AI for your snake

![Snake Game](content/snake_game.gif) <!-- .element: class="fragment" data-fragment-index="1" -->

...
- What is battlesnake?!
- Remember that snake game you used to be able to play on your Nokia phone?
  - Battlesnake is alot like that, but... [GO TO NEXT SLIDE]

---

![Battlesnake v2](http://i.imgur.com/Oyw3jXl.gif) <!-- .element: width="60%" -->

...
- We put a BUNCH of snakes on the board, and YOU program the Snake's AI!
- Epic AI battle to the death
- March 4th at the conference center
  - We had too many people last year, so we had to upgrade our venue (over 460 signups so far!)

---

## Who is Battlesnake for?

- interested in technology?
- non-programmers
- programmers of all skill levels
- teams consist of 2-5 people
- individuals are welcome to compete solo

...
- Reinforce that literally _anyone_ can participate in and have fun at Battlesnake

---

## Where is Battlesnake?

<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d5295.656450024255!2d-123.36646983071856!3d48.42144202091193!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xd79ebbb26089dbd6!2sVictoria+Conference+Centre!5e0!3m2!1sen!2sca!4v1487123899505" width="800" height="550" frameborder="0" style="border:0" allowfullscreen></iframe>

...
- Conference center on the map

---

## Divisions

![Classic Division](https://static1.squarespace.com/static/583102acff7c504696a7009b/t/58683e2346c3c4a162ee9a29/1483226666696/?format=500w)
![Advanced Division](https://static1.squarespace.com/static/583102acff7c504696a7009b/t/58683e331b631bf419079e9e/1483226683992/BS-HARD.png?format=500w)

...
- Divisions this year, changes from previous years
  - No coins this year, no random walls either
  - Divisions only to separate beginner and advanced snakes for even playing grid, otherwise virtually the same

---

## Bounty Snakes

![](https://static1.squarespace.com/static/583102acff7c504696a7009b/t/5867371d8419c2e34222d2ce/1483159345552/?format=500w)

...
- Each Bounty Snake will have different rules for defeat, details will be announced during Orientation

---

# Prizes

## GRAND PRIZE: $1,000 <!-- .element: class="fragment" data-fragment-index="1" -->

### SECOND PLACE: $750 <!-- .element: class="fragment" data-fragment-index="2" -->

#### THIRD PLACE: $500 <!-- .element: class="fragment" data-fragment-index="2" -->

---

## Coming Prepared

Bring your own
- laptop
- team
- resources @ battlesnake.io

...
- Don't go into detail, just highlight the points

===

## Things you'll need to know

- Host a web server
- Collaborate on code

...
- Heroku is a great starting point, Digital Ocean and AWS are also good
- You don't have to use it, but git is a great way to collaborate git-scm.com
  - Github makes this easy!
- As far as editors go
  - Visual studio code
  - Atom editor

---

## The Game

- is played on a grid of variable size
- consists of up to 8-10 players on a single game board

---

![Battlesnake Game Board](http://i.imgur.com/Oyw3jXl.gif) <!-- .element: width="60%" -->

...
A game played by multiple snakes may look similar to this

---


![Battlesnake Game Board Interaction](content/game_server_interaction.png) <!-- .element: width="80%" -->

...
Talk about steps to go through to interact with the game serve


===

# Battlesnake API

https://www.battlesnake.io/docs

---

## `POST /start`

```json
{
  "width": 20,
  "height": 20,
  "game_id": "b1dadee8-a112-4e0e-afa2-2845cd1f21aa"
}
```
```json
{
  "color": "#FF0000",
  "head_url": "http://placecage.com/c/100/100",
  "name": "Cage Snake",
  "taunt": "OH GOD NOT THE BEES"
}
```

---

## `POST /move`

```json
{
  "you": "5b079dcd-0494-4afd-a08e-72c9a7c2d983",
  "width": 2,
  "turn": 0,
  "snakes": [ ],
  "height": 2,
  "game_id": "aecf53b9-c7f2-4f5d-bc3f-cd14cb8338f0",
  "food": [ ],
  "board": [ ]
}
```
```
{
  "move": "up",
  "taunt": "gotta go fast"
}
```

...

---

# Snakes

```json
{
  "taunt": "git gud",
  "name": "my-snake",
  "id": "5b079dcd-0494-4afd-a08e-72c9a7c2d983",
  "health_points": 93,
  "coords": [
    [0, 0],
    [1, 0],
    [1, 1]
  ]
}
```

...
- coords is an array of points the snake occupies
- first is the head?

---

## Board

```json
"board": [
  [
    {
      "state": "head",
      "snake": "my-snake"
    },
    {
      "state": "empty"
    }
  ],
  [ ]
]
```

...
- Board array of vectors

===

# Sample Snakes

===

![#neverforget](http://blog.sendwithus.com/wp-content/uploads/2015/02/ripinpeacechicken-500x492.png)
