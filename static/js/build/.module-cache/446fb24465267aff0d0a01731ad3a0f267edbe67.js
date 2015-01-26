/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    componentDidMount: function () {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');

        var board = new snakewithus.Board(ctx, canvas);
    },
    render: function () {
        return (
            React.createElement("canvas", null, "GAME")
        );
    }
});

var Wrapper = React.createClass({displayName: "Wrapper",
    render: function () {
        return (
            React.createElement("div", {className: "wrapper"}, 
                React.createElement(Game, null)
            )
        );
    }
});

// Trigger the first render
React.render(React.createElement(Wrapper, null), document.getElementById('wrapper'));
