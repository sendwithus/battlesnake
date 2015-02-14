/** @jsx React.DOM */

var Game = React.createClass({
    handleStart: function (isManual) {
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/start',
            data: JSON.stringify({ manual: isManual }),
            contentType: 'application/json',
        }).done(function (response) {
            console.log('Started Game', response.data);
            this.setState({ game: response.data });

            if (!isManual) {
                this.interval = setInterval(this.tick, 500);
            }
        }.bind(this));
    },
    handleClickNextTurn: function () {
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/turn'
        }).done(function (response) {
            this.handleGameState(response.data);
        }.bind(this));
    },
    handleGameState: function (gameState) {
        if (gameState.snakes.length === 0) {
            clearInterval(this.interval);
        }

        this.setState({ latestGameState: gameState });
    },
    handleClickContinuous: function () {
        this.interval = setInterval(this.handleClickNextTurn, 400);
    },
    tick: function () {
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId + '/gamestates/latest'
        }).done(function (response) {
            this.handleGameState(response.data);
        }.bind(this));
    },
    componentDidMount: function () {
        var canvas = this.refs.canvas.getDOMNode();
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId
        }).done(function (response) {
            this.setState({ game: response.data });
            this.tick();
        }.bind(this));
    },
    getBoard: function () {
        if (!this.board) {
            var canvas = this.refs.canvas.getDOMNode();
            var ctx = canvas.getContext('2d');
            this.board = new Board(ctx, canvas);
        }

        return this.board;
    },
    componentDidUpdate: function (prevProps, prevState) {
        if (!this.state.latestGameState) { return; }

        var board = this.getBoard();

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
                        game={this.state.game}
                        latestGameState={this.state.latestGameState}
                        continueous={this.handleClickContinuous}
                        startAutomated={this.handleStart.bind(null, false)}
                        startManual={this.handleStart.bind(null, true)}
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
                return <li key={'a_' + i}>{snake.name} ({snake.coords.length})</li>;
            });
            var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
                return <li key={'d_' + i}>{snake.name} ({snake.coords.length})</li>;
            });
        }
        var buttons;

        if (!this.props.game) {
            buttons = ('');
        } else if (this.props.game.state === 'created') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.startAutomated}>
                        Start Automated
                    </button>
                    <br />
                    <br />
                    <button className="btn btn-success stretch" onClick={this.props.startManual}>
                        Start Debug
                    </button>
                </div>
            );
        } else if (this.props.game.state === 'manual') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.nextTurn}>
                        Next Turn
                    </button>
                    {
                    /*<br />
                    <br />
                    <button className="btn btn-success stretch" onClick={this.props.continueous}>
                        Continueous
                    </button>
                    */}
                </div>
            );
        } else {
            // no buttons for real games
        }

        return (
            <div className="game-sidebar sidebar-inner">
                <h3>{this.props.gameId}</h3>

                <p>Living Snakes</p>
                <ul>{snakes}</ul>

                <p>Dead Snakes</p>
                <ul>{deadSnakes}</ul>

                <hr />

                {buttons}
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
            var path = '/play/games/' + game._id
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
            window.location = '/play/games/' + response.data.game._id;
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
                <div className="form-group" key={'url_' + i}>
                    <input type="text"
                        className="form-control"
                        value={this.state.snakeUrls[i]}
                        name="snake-url"
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

