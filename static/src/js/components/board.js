/**
 *  Main game board class
 */

export default class Board {

  constructor (ctx, canvas) {
    this.ctx = ctx;
    this.canvas = canvas;
    this.dimensions = null;
    this.snakeCache = {};
    this.gameState = {
      id: 'None',
      board: [],
      snakes: [],
      turn: 0
    }

    this.testPlayer = false;
    this.isStarted = false;
    this.lastTick = 0;
    this.devicePixelRatio = 1.25;
  }

  init (width, height) {
    console.log('INIT BOARD', width, height);
    this.gameState = null;
    this.dimensions = [ width, height ];

    this.resize();

    // <RENDER_IMAGES_HACK>
    let interval = setInterval(() => {
        this.update(this.gameState);
    }, 50);

    setTimeout(() => {
        clearInterval(interval);
    }, 5000);
    // </RENDER_IMAGES_HACK>

    window.onresize = this.resize;
  }

  resize () {
    let board = this.canvas.parentNode;

    let width  = board.clientWidth - 40;
    let height = window.innerHeight - 105;

    let size1 = Math.ceil(width / this.dimensions[0]);
    let size2 = Math.ceil(height / this.dimensions[1]);

    this.SQUARE_SIZE = Math.min(size1, size2);

    if (window.devicePixelRatio > this.devicePixelRatio) {
      this.SQUARE_SIZE = this.SQUARE_SIZE * 2;
    }

    this.canvas.width  = this.SQUARE_SIZE * this.dimensions[0];
    this.canvas.height = this.SQUARE_SIZE * this.dimensions[1];

    if (window.devicePixelRatio > this.devicePixelRatio) {
      this.canvas.style.width = (this.canvas.width / 2) + 'px';
      this.canvas.style.height = (this.canvas.height / 2) + 'px';
      this.ctx.scale(2,2); // fix blurry board on retina screens
    }

    if (this.gameState) { this.update(this.gameState); }
  }

  beginAnimation () {
    let that = this;
    this.animate();
    this.animationLoop = setInterval(function () {
      that.animate.call(that);
    }, 300);
  }

  animate () {
    let boardData = this.gameState.board;
    for (var x = 0; x < boardData.length; x++) {
      let col = boardData[x];
      for (var y = 0; y < col.length; y++) {
        let square = col[y];
        let color = generateColor();
        color = makeNonGray(color, 150);
        let colorStr = 'rgb(' + color.join(',') + ')';
        this.fillSquare(x, y, colorStr);
      }
    }
  }

  update (gameState) {
    this.gameState = gameState;

    this.canvas.width = this.canvas.width;

    let boardData = gameState.board;

    for (var x = 0; x < boardData.length; x++) {
      let col = boardData[x];
      for (var y = 0; y < col.length; y++) {
        let square = col[y];
        this.drawSquare(x, y, square);
      }
    }

    if (typeof this.updateCallback === 'function') {
      this.updateCallback(gameState);
    }

    // if (this.isGameOver()) {
    //   clearInterval(this.loop);
    //   this.beginAnimation();
    // }
  }

  drawSquare (x, y, square) {
    if (square.length > 1) {
      console.error(
        'ERROR: More than one object returned at square', x, y
      );
    }

    // console.log('DRAWING SQUARE', x, y, square.state);
    let snake;
    let head;

    this.fillSquare(x, y, snakewithus.COLORS.EMPTY);

    if (square.state === snakewithus.SQUARE_TYPES.EMPTY) {
      // Nothing
    }

    // Draw body
    else if (square.state === snakewithus.SQUARE_TYPES.SNAKE) {
      snake = this.getSnake(square.snake || square.snake_id);
      this.fillSquare(x, y, snake.getColor());
    }

    // Draw head
    else if (square.state === snakewithus.SQUARE_TYPES.SNAKE_HEAD) {
      snake = this.getSnake(square.snake || square.snake_id);
      head = snake.getHeadImage();
      if (head) {
        this.drawImage(x, y, head);
      } else {
        this.fillSquare(x, y, snake.getHeadColor());
      }
    }

    // Draw food
    else if (square.state === snakewithus.SQUARE_TYPES.FOOD) {
      this.fillCircle(x, y, snakewithus.COLORS.FOOD);
    }

    else {
      console.error('INVALID SQUARE TYPE', square.state);
    }
  }

  getSnake (id) {
    let snake_data = null;

    if (this.snakeCache[id]) { return this.snakeCache[id]; }

    for (var i = 0; i < this.gameState.snakes.length; i++) {
      let s = this.gameState.snakes[i];
      if ((s.name || s.id) === id) {
        snake_data = s;
        break;
      }
    }

    let snake = new Snake(snake_data);
    this.snakeCache[id] = snake;
    return snake;
  }

  getBoardDimensions (board) {
    return this.dimensions;
  }

  fillSquare (x, y, color) {
    let xStart = x * this.SQUARE_SIZE;
    let yStart = y * this.SQUARE_SIZE;

    this.ctx.beginPath();
    this.ctx.rect(
      xStart + snakewithus.SQUARE_PADDING,
      yStart + snakewithus.SQUARE_PADDING,
      this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2,
      this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2
    );
    this.ctx.fillStyle = color;
    this.ctx.fill();
  }

  drawImage (x, y, img) {
    let size = this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2;

    let xStart = x * this.SQUARE_SIZE + snakewithus.SQUARE_PADDING;
    let yStart = y * this.SQUARE_SIZE + snakewithus.SQUARE_PADDING;

    this.ctx.drawImage(img, xStart, yStart, size, size);
  }

  fillCircle (x, y, color) {
    let halfSquare = Math.round(this.SQUARE_SIZE / 2);
    let xCenter = x * this.SQUARE_SIZE + halfSquare;
    let yCenter = y * this.SQUARE_SIZE + halfSquare;
    let radius = this.SQUARE_SIZE / 2 * snakewithus.FOOD_SIZE;

    this.ctx.beginPath();
    this.ctx.arc(xCenter, yCenter, radius, 0, 2 * Math.PI);
    this.ctx.fillStyle = color;
    this.ctx.fill();
  }

}
