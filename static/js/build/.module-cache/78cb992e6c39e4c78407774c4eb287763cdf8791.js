/** @jsx React.DOM */

var App = React.createClass({displayName: "App",
    mixins: [ ReactMiniRouter.RouterMixin ],
    routes: {
        '/': 'games',
        '/play': 'play',
        '/play/games': 'games',
        '/play/new': 'create',
        '/play/games/:gameId': 'game'
    },
    play: function () {
        window.location = '/play/games';
    },
    game: function (gameId) {
        return this.wrapPage(
            React.createElement(Game, {gameId: gameId})
        );
    },
    create: function () {
        return this.wrapPage(
            React.createElement(GameCreate, null)
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
