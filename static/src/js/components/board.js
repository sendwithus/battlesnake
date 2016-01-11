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
  }

  init (width, height, gameState) {
    this.gameState = gameState;
    this.dimensions = [ width, height ];

    this.resize.call(this);
    window.onresize = this.resize.bind(this);
  }

  resize () {
    var board = this.container.parentNode;

    var width  = board.clientWidth - 40;
    var height = window.innerHeight - 105;

    this.width = width;
    this.height = height;

    var size1 = Math.ceil(width / this.dimensions[0]);
    var size2 = Math.ceil(height / this.dimensions[1]);

    this.SQUARE_SIZE = Math.min(size1, size2) - 2;

    d3.select(this.container).select('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    if (this.gameState) { this.update(this.gameState); }
  }

  update (gameState) {
    this.gameState = gameState;

    var colours = {
        body: snakewithus.SQUARE_TYPES.SNAKE,
        empty: snakewithus.COLORS.EMPTY,
        food: snakewithus.COLORS.EMPTY,
        snake_head: snakewithus.SQUARE_TYPES.SNAKE_HEAD,
        gold: snakewithus.SQUARE_TYPES.GOLD
      },
      boardData = gameState.board,
      bitWidth = this.SQUARE_SIZE,
      spacing = snakewithus.SQUARE_PADDING,
      rows = this.svg.selectAll('g.row').data(boardData),
      cells = rows.selectAll('rect.cell').data(_.identity),
      food = this.svg.selectAll('circle.food').data(gameState.food),
      xOffs = 0,
      yOffs = 0;

    if (this.width > this.height) {
      xOffs = (this.width - this.SQUARE_SIZE * this.gameState.width) / 2;
    } else {
      yOffs = (this.height - this.SQUARE_SIZE * this.gameState.height) / 2;
    }

    // enters
    rows.enter()
      .append('g')
      .attr('class', 'row');
    cells.enter().append('rect')
      .attr('class', 'cell')
      .attr('width', bitWidth - spacing)
      .attr('height', bitWidth - spacing)
      .attr('fill', function(d){ return colours[d.state] });
    food.enter().append('circle')
      .attr('class', 'food')
      .attr('r', (this.SQUARE_SIZE / 2) - spacing)
      .attr('fill', snakewithus.COLORS.FOOD);

    // transitions
    rows.transition().duration(0);
    cells.transition()
      .duration(0)
      .attr('x', function(d, x, y){ return y * bitWidth + xOffs; })
      .attr('y', function(d, x, y){ return x * bitWidth + yOffs; })
      .attr('fill', function(d){ return colours[d.state] });
    food.transition()
      .each('start', function(d) {
        d3.select(this).attr('r', 0);
      })
      .each('end', function(d) {
        d3.select(this).attr('r', (bitWidth / 2) - spacing);
      })
      .duration(0)
      .attr('cx', function(d){ return d[0] * bitWidth + xOffs + bitWidth / 2 - spacing / 2; })
      .attr('cy', function(d){ return d[1] * bitWidth + yOffs + bitWidth / 2 - spacing / 2; });

    food.exit().remove();
  }
}
