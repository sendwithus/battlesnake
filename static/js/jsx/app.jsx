/** @jsx React.DOM */

var App = React.createClass({
    mixins: [ ReactMiniRouter.RouterMixin ],
    routes: {
        '/': 'games',
        '/play/watch': 'games',
        '/play/watch/:gameId': 'watch'
    },
    watch: function (gameId) {
        return this.wrapPage(
            <Game gameId={gameId} />
        );
    },
    games: function () {
        return this.wrapPage(
            <GameList />
        );
    },
    wrapPage: function (page) {
        return (
            <div>
                <Navbar />
                <div className="container-fluid">
                    {page}
                </div>
            </div>
        );
    },

    render: function () {
        return this.renderCurrentRoute();
    }
});

// Trigger the first render
window.onload = function () {
    React.render(<App history={true} />, document.getElementById('app'));
};
