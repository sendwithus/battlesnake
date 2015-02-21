/**
 *  Main game board class
 */
var Board = function (ctx, canvas) {
  this.ctx = ctx;
  this.canvas = canvas;
  this.dimensions = null;
  this.snakeCache = { };
  this.gameState = {
    id: 'None',
    board: [ ],
    snakes: [ ],
    turn: 0
  };

  this.testPlayer = false;
  this.isStarted = false;
  this.lastTick = 0;
  this.devicePixelRatio = 1.25;
};

Board.prototype.resize = function() {
  var board = this.canvas.parentNode;

  var width  = board.clientWidth - 40;
  var height = window.innerHeight - 105;

  var size1 = Math.ceil(width / this.dimensions[0]);
  var size2 = Math.ceil(height / this.dimensions[1]);

  this.SQUARE_SIZE = Math.min(size1, size2);

  if (window.devicePixelRatio > this.devicePixelRatio) {
    this.SQUARE_SIZE = this.SQUARE_SIZE * 2;
  }

  this.canvas.width  = this.SQUARE_SIZE * this.dimensions[0];
  this.canvas.height = this.SQUARE_SIZE * this.dimensions[1];
  this.canvas.style.width = (this.canvas.width / 2) + 'px';
  this.canvas.style.height = (this.canvas.height / 2) + 'px';

  if (window.devicePixelRatio > this.devicePixelRatio) {
    this.ctx.scale(2,2); // fix blurry board on retina screens
  }

  if (this.gameState) { this.update(this.gameState); }
};

Board.prototype.init = function (width, height) {
  console.log('INIT BOARD', width, height);
  this.gameState = null;
  this.dimensions = [ width, height ];

  this.resize();

  // <RENDER_IMAGES_HACK>
  var interval = setInterval(function () {
      this.update(this.gameState);
  }.bind(this), 50);

  setTimeout(function () {
      clearInterval(interval);
  }.bind(this), 5000);
  // </RENDER_IMAGES_HACK>

  window.onresize = this.resize.bind(this);
};

Board.prototype.beginAnimation = function () {
  var that = this;
  this.animate();
  this.animationLoop = setInterval(function () {
    that.animate.call(that);
  }, 300);
};

Board.prototype.animate = function () {
  var boardData = this.gameState.board;
  for (var x = 0; x < boardData.length; x++) {
    var col = boardData[x];
    for (var y = 0; y < col.length; y++) {
      var square = col[y];
      var color = generateColor();
      color = makeNonGray(color, 150);
      var colorStr = 'rgb(' + color.join(',') + ')';
      this.fillSquare(x, y, colorStr);
    }
  }
};

Board.prototype.update = function (gameState) {
  this.gameState = gameState;

  this.canvas.width = this.canvas.width;

  var boardData = gameState.board;

  for (var x = 0; x < boardData.length; x++) {
    var col = boardData[x];
    for (var y = 0; y < col.length; y++) {
      var square = col[y];
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
};

Board.prototype.drawSquare = function (x, y, square) {
  if (square.length > 1) {
    console.error(
      'ERROR: More than one object returned at square', x, y
    );
  }

  // console.log('DRAWING SQUARE', x, y, square.state);
  var snake;
  var head;

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
};

Board.prototype.getSnake = function (id) {
  var snake_data = null;

  if (this.snakeCache[id]) { return this.snakeCache[id]; }

  for (var i = 0; i < this.gameState.snakes.length; i++) {
    var s = this.gameState.snakes[i];
<<<<<<< HEAD
    if (s.id === id) {
=======
    if ((s.name || s.id) === id) {
>>>>>>> 43d303f04912b7633b3a04a093472ecffbfec0b7
      snake_data = s;
      break;
    }
  }

  var snake = new Snake(snake_data);
  this.snakeCache[id] = snake;
  return snake;
};

Board.prototype.getBoardDimensions = function (board) {
  return this.dimensions;
};

Board.prototype.fillSquare = function (x, y, color) {
  var xStart = x * this.SQUARE_SIZE;
  var yStart = y * this.SQUARE_SIZE;

  this.ctx.beginPath();
  this.ctx.rect(
    xStart + snakewithus.SQUARE_PADDING,
    yStart + snakewithus.SQUARE_PADDING,
    this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2,
    this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2
  );
  this.ctx.fillStyle = color;
  this.ctx.fill();
};

Board.prototype.drawImage = function (x, y, img) {
  var size = this.SQUARE_SIZE - snakewithus.SQUARE_PADDING * 2;

  var xStart = x * this.SQUARE_SIZE + snakewithus.SQUARE_PADDING;
  var yStart = y * this.SQUARE_SIZE + snakewithus.SQUARE_PADDING;

  this.ctx.drawImage(img, xStart, yStart, size, size);
};

Board.prototype.fillCircle = function (x, y, color) {
  var halfSquare = Math.round(this.SQUARE_SIZE / 2);
  var xCenter = x * this.SQUARE_SIZE + halfSquare;
  var yCenter = y * this.SQUARE_SIZE + halfSquare;
  var radius = this.SQUARE_SIZE / 2 * snakewithus.FOOD_SIZE;

  this.ctx.beginPath();
  this.ctx.arc(xCenter, yCenter, radius, 0, 2 * Math.PI);
  this.ctx.fillStyle = color;
  this.ctx.fill();
};
