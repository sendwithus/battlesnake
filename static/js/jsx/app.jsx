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
            <div className="row">
                <div className="col-md-9">
                    <Game gameId={gameId} />
                </div>
                <div className="col-md-3 sidebar">
                    <Sidebar gameId={gameId} />
                </div>
            </div>
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
