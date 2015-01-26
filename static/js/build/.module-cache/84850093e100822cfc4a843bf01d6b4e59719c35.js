/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    componentDidMount: function () {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
    },
    render: function () {
        return (
            React.createElement("canvas", null, "GAME")
        );
    }
});

