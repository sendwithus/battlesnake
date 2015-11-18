/** @jsx React.DOM */

var react = require('react');
//
// var Board = require('../board');

module.exports = React.createClass({displayName: "exports",
    render: function () {
        return (
            React.createElement("div", {className: "wrapper"}, 
                React.createElement("h1", null, "HELLO WORLD")
            )
        );
    }
});

// Trigger the first render
// React.render(<Wrapper />, document.getElementById('wrapper'));
