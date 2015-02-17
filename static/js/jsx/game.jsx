/** @jsx React.DOM */

var navigate = ReactMiniRouter.navigate;

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
            this.checkInterval();
        }.bind(this));
    },
    handleReplay: function () {
        console.log('Started Replay');
        var url = '/api/games/' + this.props.gameId + '/gamestates';

        $.ajax({ type: 'GET', url: url }).done(function (response) {
            var framesCompleted = 0;
            var gameStates = response.data;

            var next = function () {
                this.handleGameState(gameStates[gameStates.length - framesCompleted - 1]);
                if (++framesCompleted < response.data.length) {
                    setTimeout(next, 250);
                }
            }.bind(this);

            next();
        }.bind(this));

        this.setState({ isReplay: true });
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

        if (this.isMounted()) {
            this.setState({ latestGameState: gameState });
        } else {
            // If we're no longer on this page...
            this.interval = clearInterval(this.interval);
        }
    },
    handleClickContinuous: function () {
        this.interval = setInterval(this.handleClickNextTurn, 400);
    },
    tick: function (callback) {
        var url = '/api/games/' + this.props.gameId + '/gamestates/latest';

        $.ajax({ type: 'GET', url: url }).done(function (response) {
            this.handleGameState(response.data);
            callback && callback();
        }.bind(this));
    },
    checkInterval: function () {
        // Start the ticker if it hasen't already
        var shouldTick = this.state.game.state === 'playing' ||
                         this.state.game.state === 'ready';

        if (shouldTick && !this.interval) {
            this.interval = setInterval(this.tick, 500);
        }
    },
    componentDidMount: function () {
        var canvas = this.refs.canvas.getDOMNode();
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId
        }).done(function (response) {
            this.setState({ game: response.data });

            // Get latest game state
            this.tick(function () {
                // See if we need to tick the game
                this.checkInterval();
            }.bind(this));
        }.bind(this));
    },
    componentDidUpdate: function (prevProps, prevState) {
        if (!this.state.latestGameState) { return; }

        var board = this.getBoard();

        board.init(this.state.game.width, this.state.game.height);
        board.update(this.state.latestGameState);
    },
    getBoard: function () {
        if (!this.board) {
            var canvas = this.refs.canvas.getDOMNode();
            var ctx = canvas.getContext('2d');
            this.board = new Board(ctx, canvas);
        }

        return this.board;
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
                        isReplay={this.state.isReplay}
                        latestGameState={this.state.latestGameState}
                        continueous={this.handleClickContinuous}
                        startAutomated={this.handleStart.bind(null, false)}
                        startReplay={this.handleReplay.bind(null, false)}
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
                </div>
            );
        } else if (!this.props.isReplay && this.props.game.state === 'done') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.startReplay}>
                        Replay
                    </button>
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
                <li key={game._id}><a href={path}>{game._id} ({game.state})</a></li>
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
    _loadPastSnakes: function () {
        try {
            return JSON.parse(window.localStorage['battlesnake.snake_urls']);
        } catch (e) {
            return [ '' ];
        }
    },
    _savePastSnakes: function () {
        var json = JSON.stringify(this.state.snakeUrls);
        window.localStorage['battlesnake.snake_urls'] = json;
    },
    handleGameCreate: function (e) {
        e.preventDefault();

        var gameData = { snake_urls: this.state.snakeUrls };

        $.ajax({
            type: 'POST',
            url: '/api/games',
            data: JSON.stringify(gameData),
            contentType: 'application/json'
        }).done(function (response) {
            navigate('/play/games/' + response.data.game._id);
            this._savePastSnakes();
        }.bind(this)).error(function (xhr, textStatus, errorThrown) {
            alert(xhr.responseJSON.message);
        });
    },
    handleSubmitSnake: function (e) {
        e.preventDefault();
        var snakeUrls = this.state.snakeUrls;
        snakeUrls.push(this.state.currentSnakeUrl);
        this.setState({ snakeUrls: snakeUrls });
    },
    handleSnakeUrlChange: function (e) {
        this.setState({ currentSnakeUrl: e.target.value });
    },
    handleDeleteSnakeUrl: function (i, e) {
        var snakeUrls = this.state.snakeUrls;
        snakeUrls.splice(i, 1);
        this.setState({ snakeUrls: snakeUrls });
    },
    getInitialState: function () {
        return {
            snakeUrls: this._loadPastSnakes(),
            currentSnakeUrl: ''
        };
    },
    render: function () {
        var snakeUrls = this.state.snakeUrls.map(function (snakeUrl, i) {
            return (
                <div key={'url_' + i}>
                    <a href="#"
                        className="pull-right"
                        onClick={this.handleDeleteSnakeUrl.bind(null, i)}>
                        X
                    </a>
                    <p>{snakeUrl}</p>
                </div>
            );
        }.bind(this));

        return (
            <div className="container">
                <form onSubmit={this.handleSubmitSnake}>
                    <h2>Create Game</h2>
                    <br />
                    <div>
                        {snakeUrls}
                    </div>
                    <div className="input-group">
                        <input type="text"
                            className="form-control"
                            value={this.state.currentSnakeUrl}
                            name="snake-url"
                            placeholder="http://mysnake.herokuapp.com"
                            onChange={this.handleSnakeUrlChange}
                        />
                        <span className="input-group-btn">
                            <button type="submit"
                                    disabled={this.state.currentSnakeUrl ? false : 'on'}
                                    className="btn btn-info big form-control">
                                Add Snake
                            </button>
                        </span>
                    </div>
                    <div className="input-group">
                        <button type="button" className="btn btn-success" onClick={this.handleGameCreate}>
                            Start Game
                        </button>
                    </div>
                </form>
            </div>
        );
    }
});

