/** @jsx React.DOM */

var Canvas = React.createClass({displayName: "Canvas",
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new snakewithus.Board(ctx, canvas);
    },
    render: function () {
        return (
            React.createElement("canvas", null, "Failed to load canvas!")
        );
    }
});

var Wrapper = React.createClass({displayName: "Wrapper",
    render: function () {
        return (
            React.createElement("div", {className: "wrapper"}, 
                React.createElement(Canvas, null)
            )
        );
    }
});

// Trigger the first render
React.render(React.createElement(Wrapper, null), document.getElementById('wrapper'));
