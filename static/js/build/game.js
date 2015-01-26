/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
        board.init(sampleBoardData, function () { });
    },
    render: function () {
        return (
            React.createElement("canvas", null, "Your browser does not support canvas")
        );
    }
});

