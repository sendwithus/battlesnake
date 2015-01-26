/** @jsx React.DOM */

var App = React.createClass({displayName: "App",
    render: function () {
        return (
            React.createElement("div", null, 
                React.createElement(Navbar, null), 
                React.createElement("div", {className: "container-fluid"}, 
                    React.createElement("div", {className: "row"}, 
                        React.createElement("div", {className: "col-md-9"}, 
                            React.createElement(Game, null)
                        ), 
                        React.createElement("div", {className: "col-md-3 sidebar"}, 
                            React.createElement(Sidebar, null)
                        )
                    )
                )
            )
        );
    }
});

// Trigger the first render
window.onload = function () {
    React.render(React.createElement(App, null), document.getElementById('app'));
};
