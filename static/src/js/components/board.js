/**
 *  Main game board class
 */

import snakewithus from '../constants/snakewithus';

import Snake from './snake';

export default class Board {
  constructor (container) {
    this.container = container;

    this.svg = d3.select(this.container)
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    this.svg.append('defs')
      .append('pattern')
      .attr('id', 'bricks')
      .attr('patternUnits', 'userSpaceOnUse')
      .attr('width', 300)
      .attr('height', 225)
      .append('image')
      .attr('width', 300)
      .attr('height', 225)
      .attr('xlink:href', '/static/img/bricks.jpg');

    this.canvas = this.svg.append('rect')
      .attr('fill', 'none');

    this.boardGroup = this.svg.append('g');

    this.boardGroup.append('rect')
      .attr('class', 'board')
      .attr('fill', 'steelblue');

    var innerBoardGroup = this.boardGroup.append('g')
      .attr('class', 'inner-board');

    innerBoardGroup.append('rect')
      .attr('class', 'inner-board')
      .attr('fill', '#333');

    this.boardGroup.append('g')
      .attr('class', 'cell-container');
  }

  init (gameState) {
    this.gameState = gameState;

    this.resize.call(this);
    window.onresize = this.resize.bind(this);
  }

  resize () {
    var containerParent = this.container.parentNode;

    var width  = containerParent.clientWidth - 40;
    var height = window.innerHeight - 105;

    this.width = width;
    this.height = height;

    d3.select(this.container).select('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    if (this.gameState) { this.update(this.gameState); }
  }

  update (gameState) {
    this.gameState = gameState;

    var scale = Math.min(this.width / gameState.width, this.height / gameState.height),
      boardWidth = scale * gameState.width,
      boardHeight = scale * gameState.height,
      xOffs = (this.width - boardWidth) / 2,
      yOffs = (this.height - boardHeight) / 2,
      innerBoardPadding = 10,
      spacing = snakewithus.SQUARE_PADDING,
      bitWidth = (boardWidth - innerBoardPadding * 2 - spacing) / gameState.width,
      bitHeight = (boardHeight - innerBoardPadding * 2 - spacing) / gameState.height,
      boardData = gameState.board,
      deathAnimationDuration = 1000,
      explodeSize = 1000,
      rows = this.svg.select('g.inner-board').selectAll('g.row').data(boardData),
      cells = rows.selectAll('rect.cell').data(_.identity),
      //food = this.svg.select('g.inner-board').selectAll('circle.food').data(gameState.food, _.identity),
      food = d3.select(this.container).selectAll('img.food').data(gameState.food, _.identity),
      snakes = this.svg.select('g.inner-board').selectAll('g.snake').data(gameState.snakes),
      snakeBits = snakes.selectAll('rect.snakeBit').data(function(d) { return d.coords; }),
      walls = this.svg.select('g.inner-board').selectAll('rect.wall').data(gameState.walls),
      heads = d3.select(this.container).selectAll('img.head').data(gameState.snakes),
      gold = d3.select(this.container).selectAll('img.gold').data(gameState.gold);

    function isAbove(dx, dy) { return dx === 0 && dy === -1; }
    function isLeftOf(dx, dy) { return dx === -1 && dy === 0; }
    function isBelow(dx, dy) { return dx === 0 && dy === 1; }
    function isRightOf(dx, dy) { return dx === 1 && dy === 0; }

    function directionRotation(snake) {
      var rotation = 0;
      if (snake.coords.length > 1) {
        var head = _.head(snake.coords),
          neck = snake.coords[1],
          dx = head[0] - neck[0],
          dy = head[1] - neck[1];

        if (isLeftOf(dx, dy)) rotation = 270;
        else if (isBelow(dx, dy)) rotation = 180;
        else if (isRightOf(dx, dy)) rotation = 90;
      }

      return ['rotate(',rotation,'deg)'].join('');
    }

    this.canvas
      .attr('width', this.width)
      .attr('height', this.height);

    this.boardGroup.select('rect.board')
      .attr('width', boardWidth)
      .attr('height', boardHeight);

    //// center the board on the canvas
    if (Math.floor(this.width) === Math.floor(boardWidth)) {
      this.boardGroup.attr('transform', 'translate(0, ' + yOffs + ')');
    } else {
      this.boardGroup.attr('transform', 'translate(' + xOffs + ')');
    }

    this.boardGroup.select('g.inner-board')
      .attr('transform', 'translate(' + innerBoardPadding + ',' + innerBoardPadding + ')');

    this.boardGroup.select('rect.inner-board')
      .attr('width', boardWidth - innerBoardPadding * 2)
      .attr('height', boardHeight - innerBoardPadding * 2);

    // enters
    rows.enter().append('g')
      .attr('class', 'row');
    cells.enter().append('rect')
      .attr('class', 'cell');
    //food.enter().append('circle')
    //  .attr('class', 'food')
    //  .attr('r', 0)
    //  .attr('fill', snakewithus.COLORS.FOOD);
    food.enter().append('img')
      .attr('class', 'food')
      .attr('width', bitWidth - spacing)
      .attr('width', bitWidth - spacing)
      .attr('fill', snakewithus.COLORS.FOOD);
    gold.enter().append('img')
      .attr('class', 'gold')
      .attr('width', bitWidth - spacing)
      .attr('width', bitWidth - spacing)
      .attr('fill', snakewithus.COLORS.GOLD);
    walls.enter().append('rect')
      .attr('class', 'wall')
      .attr('width', bitWidth - spacing)
      .attr('height', 0)
      .attr('fill', 'steelblue');
    snakes.enter().append('g')
      .attr('class', 'snake');
    snakeBits.enter()
      .append('rect')
      .attr('class', 'snakeBit');
    heads.enter().append('img')
      .attr('class', 'head');

    // transitions
    rows.transition().duration(0);
    cells.transition().duration(0)
      .attr('x', function(d, x, y){ return y * bitWidth + spacing; })
      .attr('y', function(d, x, y){ return x * bitHeight + spacing; })
      .attr('width', bitWidth - spacing)
      .attr('height', bitHeight - spacing)
      .attr('fill', _.constant(snakewithus.COLORS.EMPTY));
    //food.transition()
    //  .duration(250)
    //  .attr('r', (bitWidth / 3) - spacing)
    //  .attr('cx', function(d){ return spacing + d[0] * bitWidth + bitWidth / 2 - spacing / 2; })
    //  .attr('cy', function(d){ return spacing + d[1] * bitHeight + bitWidth / 2 - spacing / 2; });
    walls.transition()
      .duration(100)
      .attr('x', function(d) { return spacing + d[0] * bitWidth })
      .attr('y', function(d) { return spacing + d[1] * bitHeight })
      .attr('width', bitWidth - spacing)
      .attr('height', bitHeight - spacing);
    snakes.transition().duration(0);
    snakeBits.transition().duration(0)
      .attr('x', function(d) { return spacing + d[0] * bitWidth })
      .attr('y', function(d) { return spacing + d[1] * bitHeight })
      .attr('width', bitWidth - spacing)
      .attr('height', bitHeight - spacing)
      .attr('fill', function(d, i, n) {
        if (i === 0) {
          return snakewithus.COLORS.EMPTY;
        } else {
          return gameState.snakes[n].color;
        }
      });
    heads.transition().duration(0)
      .attr('src', function(d) { return d.head; })
      .attr('width', bitWidth - spacing)
      .attr('height', bitHeight - spacing)
      .style('position', 'absolute')
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d.coords[0][0] * bitWidth + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d.coords[0][1] * bitHeight + 'px'; })
      .style('transform', directionRotation);
    gold.transition().duration(0)
      .attr('src', '/static/img/img-coin.gif')
      .style('border-radius', '100%')
      .attr('width', bitWidth - spacing - 10)
      .attr('height', bitHeight - spacing - 10)
      .style('position', 'absolute')
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d[0] * bitWidth  + 5 + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d[1] * bitHeight + 5 + 'px'; });
    food.transition().duration(0)
      .attr('src', '/static/img/eco-green-apple.png')
      .attr('width', bitWidth - spacing)
      .attr('height', bitHeight - spacing)
      .style('position', 'absolute')
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d[0] * bitWidth + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d[1] * bitHeight + 'px'; });

    // exits
    food.exit().remove();
    gold.exit().remove();
    walls.exit().remove();
    snakes.exit().transition()
      .duration(deathAnimationDuration).remove();
    snakes.exit().selectAll('rect.snakeBit').transition()
      .duration(deathAnimationDuration)
      .attr('width', explodeSize)
      .attr('height', explodeSize)
      .attr('x', function(d) { return spacing + d[0] * bitWidth - (explodeSize / 2) })
      .attr('y', function(d) { return spacing + d[1] * bitHeight - (explodeSize / 2) })
      .style('opacity', 0);
    snakeBits.exit().transition()
      .duration(deathAnimationDuration).remove();
    heads.exit().transition()
      .duration(deathAnimationDuration)
      .attr('width', explodeSize)
      .attr('height', explodeSize)
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d.coords[0][0] * bitWidth - (explodeSize / 2) + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d.coords[0][1] * bitHeight - (explodeSize / 2) + 'px'; })
      .style('opacity', 0)
      .remove();
  }
}
