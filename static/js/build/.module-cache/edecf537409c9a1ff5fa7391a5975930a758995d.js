/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    render: function () {
        return (
            React.createElement("nav", {className: "navbar navbar-inverse"}, 
                React.createElement("div", {className: "container"}, 
                    React.createElement("div", {className: "navbar-header"}, 
                        React.createElement("a", {className: "navbar-brand", href: "#"}, "Project name")
                    ), 
                    React.createElement("div", {className: "collapse navbar-collapse"}, 
                        React.createElement("ul", {className: "nav navbar-nav"}, 
                            React.createElement("li", {className: "active"}, React.createElement("a", {href: "#"}, "Home")), 
                            React.createElement("li", null, React.createElement("a", {href: "#about"}, "About")), 
                            React.createElement("li", null, React.createElement("a", {href: "#contact"}, "Contact"))
                        )
                    )
                )
            )
        );
    }
});

var Wrapper = React.createClass({displayName: "Wrapper",
    render: function () {
        return (
            React.createElement("div", {className: "wrapper"}, 
                React.createElement(Navbar, null)
            )
        );
    }
});

// Trigger the first render
React.render(React.createElement(Wrapper, null), document.getElementById('wrapper'));
