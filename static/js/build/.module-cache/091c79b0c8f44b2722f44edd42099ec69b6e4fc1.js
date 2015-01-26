/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    render: function () {
        return (
            React.createElement("h1", null, "GAME")
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
