const snakewithus = {
  MOVE_DELTA: 0,
  SQUARE_PADDING: 2,
  FOOD_SIZE: 0.5,
  HEAD_OPACITY: 1,
  BODY_OPACITY: 0.5,
  SQUARE_TYPES: {
    EMPTY: 'empty',
    SNAKE: 'body',
    SNAKE_HEAD: 'head',
    FOOD: 'food',
    GOLD: 'gold',
    WALL: 'wall'
  },
  DIRECTIONS: {
    NORTH: 'n',
    EAST: 'e',
    SOUTH: 's',
    WEST: 'w'
  },
  STATUS: {
    ALIVE: 'alive',
    DEAD: 'dead'
  },
  COLORS: {
    FOOD: '#E6D560',
    EMPTY: 'rgba(0, 0, 0, 0.2)',
    GOLD: 'rgba(255, 215, 0, 0.2)',
    WALL: 'rgba(0, 0, 0, 1)'
  },
  MAX_COLOR: 255,
  MIN_COLOR: 120,
  BORDER_CHANGE: 4,
  KEYS: {
    UP: 38,
    DOWN: 40,
    LEFT: 37,
    RIGHT: 39
  }
}

export default snakewithus;
