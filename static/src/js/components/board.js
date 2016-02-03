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
      .attr('fill', 'url(#bricks)');

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

    var innerBoardPadding = 10,
      boardWidth = Math.min(this.width, this.height),
      xOffs = (this.width - boardWidth) / 2,
      yOffs = (this.height - boardWidth) / 2;

    this.canvas
      .attr('width', this.width)
      .attr('height', this.height);

    this.boardGroup.select('rect.board')
      .attr('width', boardWidth)
      .attr('height', boardWidth);

    // center the board on the canvas
    if (this.width > this.height) {
      this.boardGroup.attr('transform', 'translate(' + xOffs + ')');
    } else {
      this.boardGroup.attr('transform', 'translate(0, ' + yOffs + ')');
    }

    this.boardGroup.select('g.inner-board')
      .attr('transform', 'translate(' + innerBoardPadding + ',' + innerBoardPadding + ')');

    this.boardGroup.select('rect.inner-board')
      .attr('width', boardWidth - innerBoardPadding * 2)
      .attr('height', boardWidth - innerBoardPadding * 2);



    var colours = {
        body: snakewithus.SQUARE_TYPES.SNAKE,
        empty: snakewithus.COLORS.EMPTY,
        food: snakewithus.COLORS.EMPTY,
        snake_head: snakewithus.SQUARE_TYPES.SNAKE_HEAD,
        gold: snakewithus.SQUARE_TYPES.GOLD,
        wall: snakewithus.SQUARE_TYPES.WALL
      },
      boardData = gameState.board,
      spacing = snakewithus.SQUARE_PADDING,
      bitWidth = (boardWidth - spacing - innerBoardPadding * 2) / gameState.width,
      rows = this.svg.select('g.inner-board').selectAll('g.row').data(boardData),
      cells = rows.selectAll('rect.cell').data(_.identity),
      food = this.svg.select('g.inner-board').selectAll('circle.food').data(gameState.food),
      snakes = this.svg.select('g.inner-board').selectAll('g.snake').data(gameState.snakes),
      snakeBits = snakes.selectAll('rect.snakeBit').data(function(d) { return d.coords; }),
      walls = this.svg.select('g.inner-board').selectAll('rect.wall').data(gameState.walls),
      heads = d3.select(this.container).selectAll('img.head').data(gameState.snakes),
      gold = d3.select(this.container).selectAll('img.gold').data(gameState.gold);

    // enters
    rows.enter().append('g')
      .attr('class', 'row');
    cells.enter().append('rect')
      .attr('class', 'cell');
    food.enter().append('circle')
      .attr('class', 'food')
      .attr('fill', snakewithus.COLORS.FOOD);
    gold.enter().append('img')
      .attr('class', 'gold')
      .attr('fill', snakewithus.COLORS.GOLD);
    walls.enter().append('rect')
      .attr('class', 'wall')
      .attr('fill', 'url(#bricks)');
    snakes.enter().append('g')
      .attr('class', 'snake');
    snakeBits.enter().append('rect')
      .attr('class', 'snakeBit');
    heads.enter().append('img')
      .attr('class', 'head');

    // transitions
    rows.transition().duration(0);
    cells.transition().duration(0)
      .attr('x', function(d, x, y){ return spacing + y * bitWidth; })
      .attr('y', function(d, x, y){ return spacing + x * bitWidth; })
      .attr('width', bitWidth - spacing)
      .attr('height', bitWidth - spacing)
      .attr('fill', _.constant(snakewithus.COLORS.EMPTY));
    food.transition()
      .each('start', function() {
        d3.select(this).attr('r', 0);
      })
      .each('end', function() {
        d3.select(this).attr('r', (bitWidth / 3) - spacing);
      })
      .duration(0)
      .attr('cx', function(d){ return spacing + d[0] * bitWidth + bitWidth / 2 - spacing / 2; })
      .attr('cy', function(d){ return spacing + d[1] * bitWidth + bitWidth / 2 - spacing / 2; });
    walls.transition()
      .duration(0)
      .attr('x', function(d) { return spacing + d[0] * bitWidth })
      .attr('y', function(d) { return spacing + d[1] * bitWidth })
      .attr('width', bitWidth - spacing)
      .attr('height', bitWidth - spacing);
    snakes.transition().duration(0);
    snakeBits.transition().duration(0)
      .attr('x', function(d) { return spacing + d[0] * bitWidth })
      .attr('y', function(d) { return spacing + d[1] * bitWidth })
      .attr('width', bitWidth - spacing)
      .attr('height', bitWidth - spacing)
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
      .attr('height', bitWidth - spacing)
      .style('position', 'absolute')
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d.coords[0][0] * bitWidth + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d.coords[0][1] * bitWidth + 'px'; });
    gold.transition().duration(0)
      .attr('src', '/static/img/img-coin.gif')
      .style('border-radius', '100%')
      .attr('width', bitWidth - spacing)
      .attr('height', bitWidth - spacing)
      .style('position', 'absolute')
      .style('left', function(d) { return xOffs + innerBoardPadding + spacing + 15 + d[0] * bitWidth + 'px'; })
      .style('top', function(d) { return yOffs + innerBoardPadding + spacing + d[1] * bitWidth + 'px'; });

    // exits
    food.exit().remove();
    gold.exit().remove();
    walls.exit().remove();
    snakes.exit().remove();
    snakeBits.exit().remove();
    heads.exit().remove();
  }
}
