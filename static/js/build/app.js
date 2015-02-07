/** @jsx React.DOM */

var App = React.createClass({displayName: "App",
    mixins: [ ReactMiniRouter.RouterMixin ],
    routes: {
        '/': 'games',
        '/play/watch': 'games',
        '/play/watch/:gameId': 'watch'
    },
    watch: function (gameId) {
        return this.wrapPage(
            React.createElement(Game, {gameId: gameId})
        );
    },
    games: function () {
        return this.wrapPage(
            React.createElement(GameList, null)
        );
    },
    wrapPage: function (page) {
        return (
            React.createElement("div", null, 
                React.createElement(Navbar, null), 
                React.createElement("div", {className: "container-fluid"}, 
                    page
                )
            )
        );
    },

    render: function () {
        return this.renderCurrentRoute();
    }
});

// Trigger the first render
window.onload = function () {
    React.render(React.createElement(App, {history: true}), document.getElementById('app'));
};
