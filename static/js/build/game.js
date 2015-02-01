/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    componentDidMount: function () {
        var canvas = this.getDOMNode();
        var ctx = canvas.getContext('2d');

        var board = new Board(ctx, canvas);
        board.init(sampleBoardData, function () { });
    },
    render: function () {
        return (
            React.createElement("canvas", null, "Your browser does not support canvas")
        );
    }
});

var GameList = React.createClass({displayName: "GameList",
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
                React.createElement("li", {key: game._id}, React.createElement("a", {href: path}, game._id))
            );
        });

        return (
            React.createElement("ul", null, games)
        );
    }
});

