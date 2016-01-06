sampleBoardData = {
  id: "example-game-one",
  board: [
      [ [{type: "food", id: "f1"}], [], [], [{type: "snake", id: "snake_3"}], [{type: "snake", id: "snake_3"}], [{type: "snake", id: "snake_3"}], [{type: "snake", id: "snake_3"}], [{type: "snake", id: "snake_3"}], [], [] ],
      [ [], [{type: "food", id: "f2"}], [], [], [], [], [], [{type: "snake", id: "snake_3"}], [], [] ],
      [ [], [], [{type: "food", id: "f3"}], [], [], [], [], [{type: "snake_head", id: "snake_3"}], [], [] ],
      [ [], [], [], [{type: "food", id: "f4"}], [], [], [], [], [], [] ],
      [ [{type: "snake_head", id: "snake_1"}], [], [], [], [{type: "food", id: "f5"}], [], [], [], [], [] ],
      [ [{type: "snake", id: "snake_1"}], [], [], [], [], [{type: "food", id: "f6"}], [], [], [], [] ],
      [ [{type: "snake", id: "snake_1"}], [], [], [], [], [], [{type: "food", id: "f7"}], [], [], [] ],
      [ [{type: "snake", id: "snake_1"}], [], [], [], [], [], [], [{type: "food", id: "f8"}], [], [] ],
      [ [{type: "snake", id: "snake_1"}], [], [], [], [], [], [], [], [{type: "food", id: "f9"}], [] ],
      [ [{type: "snake", id: "snake_1"}], [], [], [], [], [], [], [], [], [{type: "food", id: "f0"}] ]
  ],
  snakes: [
    {
      id: "snake_1",
      last_move: "n",
      name: "Snake One",
      facing: "n",
      status: "alive",
      message: "I AM FUCKING SNAKE ONE",
      points: {
          kills: 10,
          food: 3
      }
    }, {
      id: "snake_2",
      last_move: "w",
      name: "Snake Two",
      facing: "w",
      status: "dead",
      message: "I am dead because I suck",
      points: {
          kills: 0,
          food: 0
      }
    }, {
      id: "snake_3",
      last_move: "s",
      name: "Snake Three",
      facing: "s",
      status: "alive",
      message: "Bitchin'",
      points: {
          kills: 1,
          food: 2
      }
    }
  ],
  turn_num: 0
}

export default sampleBoardData
