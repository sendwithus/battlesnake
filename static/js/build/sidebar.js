/** @jsx React.DOM */

var Sidebar = React.createClass({displayName: "Sidebar",
    render: function () {
        return (
            React.createElement("div", {className: "sidebar-inner"}, 
                React.createElement("h3", null, "Sidebar"), 
                React.createElement("ul", null, 
                	React.createElement("li", null, "Snake 1"), 
                	React.createElement("li", null, "Snake 2"), 
                	React.createElement("li", null, "Snake 3"), 
                	React.createElement("li", null, "Snake 4")
                )
            )
        );
    }
});

