/** @jsx React.DOM */

var Wrapper = React.createClass({displayName: "Wrapper",
    render: function () {
        return (
            React.createElement("div", {className: "row"}, 
                React.createElement("div", {class: "col-md-8"}, 
                    React.createElement(Game, null)
                ), 
                React.createElement("div", {class: "col-md-4"}, 
                    React.createElement(Sidebar, null)
                )
            )
        );
    }
});

// Trigger the first render
React.render(React.createElement(Wrapper, null), document.getElementById('wrapper'));
