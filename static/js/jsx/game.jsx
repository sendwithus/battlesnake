/** @jsx React.DOM */

var Game = React.createClass({
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
        board.init(sampleBoardData, function () { });
    },
    render: function () {
        return (
            <canvas>Your browser does not support canvas</canvas>
        );
    }
});

var GameList = React.createClass({
    componentDidMount: function () {
        $.ajax({
            type: 'GET',
            url: '/api/games',
        }).done(function (response) {
            this.setState({ games: response.data });
        }.bind(this));
    },
    getInitialState: function () {
        return { games: this.props.games || [] };
    },
    render: function () {
        games = this.state.games.map(function (game, i) {
            var path = '/play/watch/' + game._id
            return (
                <li key={game._id}><a href={path}>{game._id}</a></li>
            );
        });

        return (
            <ul>{games}</ul>
        );
    }
});

