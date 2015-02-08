/** @jsx React.DOM */

var Game = React.createClass({
    handleClickNextTurn: function () {
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/turn'
        }).done(function (response) {
            console.log('Got GameState', response.data);
            var gameState = response.data;

            if (gameState.snakes.length === 0) {
                clearInterval(this.interval);
            }

            this.setState({ latestGameState: response.data });
        }.bind(this));
    },
    handleClickContinuous: function () {
        this.interval = setInterval(this.handleClickNextTurn, 400);
    },
    componentDidMount: function () {
        var canvas = this.refs.canvas.getDOMNode();
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId
        }).done(function (response) {
            console.log('Got Game', response.data);
            this.setState({ game: response.data });
            this.handleClickNextTurn();
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
                </div>
                <div className="col-md-3 sidebar">
                    <GameSidebar
                        gameId={this.props.gameId}
                        latestGameState={this.state.latestGameState}
                        continueous={this.handleClickContinuous}
                        nextTurn={this.handleClickNextTurn} />
                </div>
            </div>
        );
    }
});

var GameSidebar = React.createClass({
    render: function () {
        var snakes = '';

        if (this.props.latestGameState) {
            var snakes = this.props.latestGameState.snakes.map(function (snake, i) {
                return <li key={snake.snake_id}>{snake.name} ({snake.coords.length})</li>;
            });
            var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
                return <li key={snake.snake_id}>{snake.name} ({snake.coords.length})</li>;
            });
        }

        return (
            <div className="game-sidebar sidebar-inner">
                <h3>{this.props.gameId}</h3>
                <ul>{snakes}</ul>
                <ul>{deadSnakes}</ul>
                <button className="btn btn-success stretch" onClick={this.props.nextTurn}>
                    Next Turn
                </button>
                <br />
                <br />
                <button className="btn btn-success stretch" onClick={this.props.continueous}>
                    Continueous
                </button>
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
        var games = this.state.games.map(function (game, i) {
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

var GameCreate = React.createClass({
    handleGameCreate: function (e) {
        e.preventDefault();

        var gameData = {
            snake_urls: this.state.snakeUrls
        };

        $.ajax({
            type: 'POST',
            url: '/api/games',
            data: JSON.stringify(gameData),
            contentType: 'application/json'
        }).done(function (response) {
            window.location = '/play/watch/' + response.data.game._id;
        });
    },
    handleAddSnakeUrl: function (e) {
        var snakeUrls = this.state.snakeUrls;
        snakeUrls.push('');
        this.setState({ snakeUrls: snakeUrls });
    },
    handleSnakeUrlChange: function (i, e) {
        var snakeUrls = this.state.snakeUrls;
        snakeUrls[i] = e.target.value;

        this.setState({ snakeUrls: snakeUrls });
    },
    getInitialState: function () {
        return { snakeUrls: [''] };
    },
    render: function () {
        var snakeUrls = this.state.snakeUrls.map(function (snakeUrl, i) {
            return (
                <div className="form-group" key={i}>
                    <input type="text"
                        className="form-control"
                        value={this.state.snakeUrls[i]}
                        placeholder="http://my-snake-url.com/api"
                        onChange={this.handleSnakeUrlChange.bind(this, i)} />
                </div>
            );
        }.bind(this));

        return (
            <form onSubmit={this.handleGameCreate}>
                <h3>New Game</h3>
                {snakeUrls}
                <div className="form-group">
                    <button type="button"
                        onClick={this.handleAddSnakeUrl}
                        className="btn btn-info form-control">Add Snake</button>
                </div>
                <div className="form-group">
                    <button type="submit" className="btn btn-success form-control">
                        Create Game
                    </button>
                </div>
            </form>
        );
    }
});

