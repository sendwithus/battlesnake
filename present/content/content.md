![Sendwithus Logo](content/swu-logo.svg)

...
- Introduce ourselves.

---

![Battlesnake Logo](content/battlesnake-logo.svg)<!-- .element: width="95%" -->

...
March 4th at the conference center
Epic ai battle to the death

---

# Prerequisites

- Editor <!-- .element: class="fragment" data-fragment-index="1" -->
- Git<!-- .element: class="fragment" data-fragment-index="2" -->
- Heroku<!-- .element: class="fragment" data-fragment-index="3" -->

...
- Visual studio code
- Atom editor
- git-scm.com


===

## Fork Start Snake

<!-- .slide: data-background-image="content/gh-repo-fork-button.png" data-background-size="auto 90%" data-background-color="white" -->

...
Jem talking

---

<!-- .slide: data-background-image="content/gh-repo-forking.png" data-background-size="auto 90%" data-background-color="white" -->

---

<!-- .slide: data-background-image="content/gh-repo-clone-url.png" data-background-size="auto 90%" data-background-color="white" -->

---

## Clone your repo locally

```
$ git clone https://github.com/JemBijoux/battlesnake-node.git
$ cd battlesnake-node
```

...
- daniel talking
- once in directory: pip install, or npm install or whatever
- check the readme for instructions.

---

## Add and commit code

```
$ git add .
$ git commit -m "Mekin snek go"
```

---

## Push Changes

```
$ git push origin master
```

===

# Heroku

https://devcenter.heroku.com/articles/heroku-cli

(or google `heroku cli`)

...
- JEM!
- Get heroku installed on your system
- once installed, `heroku login` to login to heroku


---

## Create or Add

```
# Create the heroku project/remote
$ heroku create

# OR...
$ heroku git:remote -a heroku-project-name
```

...
- If you haven't made one in heroku website, `heroku create` SIMPLE!
- If you add the account in heroku through the website, you will `heroku add`
- If you made it through the heroku website, there will be instructions.

---

# Push code to Heroku

```
git push heroku master
```

... 
DANIEL


===

# HTTP

...
- Talk a bit about different methods: get, post, etc
- We are only really using `POST`

---

# JSON

...
JEM
- wrapped in curly braces
- key values
- nesting


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
