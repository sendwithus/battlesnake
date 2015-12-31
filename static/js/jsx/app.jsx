/** @jsx React.DOM */

var App = React.createClass({
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
            <Game gameId={gameId} />
        );
    },
    create: function () {
        return this.wrapPage(
            <GameCreate />
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
                <Navbar team={this.state.team} />
                <div className="container-fluid">
                    {page}
                </div>
            </div>
        );
    },
    componentDidMount: function () {
        // fetch current team data
        $.ajax({
            type: 'GET',
            url: '/api/teams/current'
        }).done(function (response) {
            this.setState({ team: response.data });
        }.bind(this));
    },

    render: function () {
        return this.renderCurrentRoute();
    }
});

// Trigger the first render
window.onload = function () {
    React.render(<App history={true} />, document.getElementById('app'));
};
