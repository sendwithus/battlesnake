/** @jsx React.DOM */

var Game = React.createClass({
    handleClickNextTurn: function () {
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/turn'
        }).done(function (response) {
            console.log('Got GameState', response.data);
            this.setState({ latestGameState: response.data });
        }.bind(this));
    },
    componentDidMount: function () {
        var canvas = this.refs.canvas.getDOMNode();
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId
        }).done(function (response) {
            console.log('Got Game', response.data);
            this.setState({ game: response.data });
        }.bind(this));
    },
    componentDidUpdate: function (prevProps, prevState) {
        if (!this.state.latestGameState) { return; }
        var canvas = this.refs.canvas.getDOMNode();
        var ctx = canvas.getContext('2d');
        var board = new Board(ctx, canvas);
        board.init(this.state.game.width, this.state.game.height);
        board.update(this.state.latestGameState);
    },
    getInitialState: function () {
        return {
            game: null,
            latestGameState: null
        };
    },
    render: function () {
        return (
            <div className="row">
                <div className="col-md-9">
                    <canvas ref="canvas">Your browser does not support canvas</canvas>
                    <button onClick={this.handleClickNextTurn}>Next</button>
                </div>
                <div className="col-md-3 sidebar">
                    <GameSidebar gameId={this.props.gameId} />
                </div>
            </div>
        );
    }
});

var GameSidebar = React.createClass({
    render: function () {
        return (
            <div className="sidebar-inner">
                <h3>{this.props.gameId}</h3>
                <ul>
                	<li>Snake 1</li>
                	<li>Snake 2</li>
                	<li>Snake 3</li>
                	<li>Snake 4</li>
                </ul>
            </div>
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
            <div>
                <h2>Current Games</h2>
                <ul>{games}</ul>
            </div>
        );
    }
});

