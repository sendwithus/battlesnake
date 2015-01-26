/** @jsx React.DOM */

var Game = React.createClass({
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
        board.init(sampleBoardData, function () { });
        board.update(sampleBoardData);
        console.log('updated');
    },
    render: function () {
        return (
            <canvas>Your browser does not support canvas</canvas>
        );
    }
});

