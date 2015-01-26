/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
        board.init({}, function () { });
    },
    render: function () {
        return (
            React.createElement("canvas", null, "GAME Hi")
        );
    }
});

