/** @jsx React.DOM */

var App = React.createClass({displayName: "App",
    handleHashChange: function (hash) {
        this.setState({ hash: hash });
    },
    componentDidMount: function () {
        this.handleHashChange(window.location.hash);
    },
    getInitialState: function () {
        return { };
    },
    render: function () {
        var page;

        if (this.state.hash === '#games') {
            page = (
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col-md-12"}, 
                        React.createElement("h1", null, "Games")
                    )
                )
            );
        } else if (this.state.hash === '#contact') {
            page = (
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col-md-12"}, 
                        React.createElement("h1", null, "Contact")
                    )
                )
            );
        } else {
            page = (
                React.createElement("div", {className: "row"}, 
                    React.createElement("div", {className: "col-md-9"}, 
                        React.createElement(Game, null)
                    ), 
                    React.createElement("div", {className: "col-md-3 sidebar"}, 
                        React.createElement(Sidebar, null)
                    )
                )
            );
        }

        return (
            React.createElement("div", null, 
                React.createElement(Navbar, {onPageChange: this.handleHashChange}), 
                React.createElement("div", {className: "container-fluid"}, 
                    page
                )
            )
        );
    }
});

// Trigger the first render
window.onload = function () {
    React.render(React.createElement(App, null), document.getElementById('app'));
};
