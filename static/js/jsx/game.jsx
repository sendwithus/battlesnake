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
    handlePause: function () {
        $.ajax({
            type: 'PUT',
            url: '/api/games/' + this.props.gameId + '/pause'
        }).done(function (response) {
            console.log('Paused Game', response.data);
            this.setState({ game: response.data });
        }.bind(this));
    },
    handleResume: function () {
        $.ajax({
            type: 'PUT',
            url: '/api/games/' + this.props.gameId + '/resume'
        }).done(function (response) {
            console.log('Resumed Game', response.data);
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
                if (++framesCompleted < response.data.length && this.state.isReplay) {
                    setTimeout(next, 350);
                }
            }.bind(this);

            next();
        }.bind(this));

        this.setState({ isReplay: true });
    },
    handleCancelReplay: function () {
        this.setState({ isReplay: false });
    },
    handleClickNextTurn: function () {
        this.setState({ isLoading: true });
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/turn'
        }).done(function (response) {
            this.handleGameState(response.data);
        }.bind(this));
    },
    handleGameState: function (gameState, ignoreEnd) {
        if (this.isMounted()) {
            console.log('GAME STATE', gameState);
            this.state.latestGameState = gameState;
            this.state.isLoading = false;

            if (gameState.is_done) {
                $('#game-summary-modal').modal('show');
                this.state.isReplay = false;
                this.state.game.state = 'done';
            }

            this.setState(this.state);
        }
    },
    handleClickContinuous: function () {
        this.interval = setInterval(this.handleClickNextTurn, 400);
    },
    tick: function (callback) {
        var url = '/api/games/' + this.props.gameId + '/gamestates/latest';
        var id = Date.now();

        $.ajax({ type: 'GET', url: url }).done(function (response) {
            this.handleGameState(response.data);
            callback && callback(response.data);
        }.bind(this));
    },
    checkInterval: function () {
        var _ = function () {
            var shouldTick = this.state.game.state === 'playing' ||
                             this.state.game.state === 'ready';
            if (!shouldTick) { return; }

            var startTimestamp = Date.now();
            this.tick(function (gameState) {
                var endTimestamp = Date.now();
                var elapsedMillis = endTimestamp - startTimestamp;

                var sleepFor = Math.max(0, this.state.game.turn_time * 1000 - elapsedMillis);

                if (this.isMounted() && shouldTick && !gameState.is_done) {
                    setTimeout(_, sleepFor);
                }

                if (gameState.is_done) {
                    this.state.game.state = 'done';
                    this.setState({ game: this.state.game });
                }
            }.bind(this));
        }.bind(this);

        _();
    },
    componentDidMount: function () {
        var canvas = this.refs.canvas.getDOMNode();
        $.ajax({
            type: 'GET',
            url: '/api/games/' + this.props.gameId
        }).done(function (response) {
            if (this.isMounted()) {
                this.setState({ game: response.data });
            }

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
        // $('#game-summary-modal').modal('show');
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
            isReplay: false,
            isLoading: false,
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
                        isLoading={this.state.isLoading}
                        latestGameState={this.state.latestGameState}
                        continueous={this.handleClickContinuous}
                        startAutomated={this.handleStart.bind(null, false)}
                        startManual={this.handleStart.bind(null, true)}
                        startReplay={this.handleReplay}
                        cancelReplay={this.handleCancelReplay}
                        pause={this.handlePause}
                        resume={this.handleResume}
                        nextTurn={this.handleClickNextTurn} />
                </div>
                <GameOverModal
                    game={this.state.game}
                    latestGameState={this.state.latestGameState}
                />
            </div>
        );
    }
});

var GameSidebarSnake = React.createClass({
    getInitialState: function () {
        return {
            lastTaunt: this.props.snake.taunt,
            tauntToShow: this.props.snake.taunt,
            tauntCount: 0,
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (this.state.lastTaunt === nextProps.snake.taunt) {
            // Taunt is the same
            this.state.tauntCount++;
        } else {
            this.state.tauntCount = 0;
            this.state.lastTaunt = nextProps.snake.taunt;
        }

        if (this.state.tauntCount > 5) {
            this.state.tauntToShow = '';
        } else {
            this.state.tauntToShow = nextProps.snake.taunt;
        }

        this.setState(this.state);
    },
    render: function () {
        var snakeStyles = {
            backgroundColor: this.props.snake.color || 'red'
        };

        var tauntStyles = {
            display: this.state.tauntToShow ? 'block' : 'none',
            opacity: 1.3 - (this.state.tauntCount / 10)
        };

        return (
            <div className="snake-block">
                <img src={this.props.snake.head_url} style={snakeStyles} />
                <h3>{this.props.snake.name} <span className="kill-reason">{this.props.snake.killReason}</span></h3>
                <div className="row meta">
                    <div className="col-md-3">
                        length: {this.props.snake.coords.length}
                    </div>
                    <div className="col-md-3">
                        kills: {this.props.snake.kills || 0}
                    </div>
                    <div className="col-md-3">
                        food: {this.props.snake.food_eaten || 0}
                    </div>
                </div>
                <div className="taunt" style={tauntStyles}>{this.state.tauntToShow}</div>
            </div>
        )
    }
});

var GameSidebar = React.createClass({
    render: function () {
        var snakes = '';

        if (!this.props.latestGameState) {
            return <div></div>;
        }

        var aliveSnakes = this.props.latestGameState.snakes.map(function (snake, i) {
            return <GameSidebarSnake key={snake.id} snake={snake} />
        });

        var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
            return <GameSidebarSnake key={snake.id} snake={snake} />
        });

        if (!deadSnakes.length) {
            deadSnakes = <p>None Yet</p>;
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
                    <button className="btn btn-info stretch" onClick={this.props.startManual}>
                        Start Debug (Step Through)
                    </button>
                </div>
            );
        } else if (this.props.game.state === 'manual') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.nextTurn} disabled={this.props.isLoading}>
                        {this.props.isLoading ? '...' : 'Play Turn ' + (this.props.latestGameState.turn + 1)}
                    </button>
                </div>
            );
        } else if (!this.props.isReplay && this.props.game.state === 'done') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.startReplay}>
                        View Replay
                    </button>
                </div>
            );
        } else if (this.props.isReplay && this.props.game.state === 'done') {
            buttons = (
                <div>
                    <button className="btn btn-info stretch" onClick={this.props.cancelReplay}>
                        Cancel Replay
                    </button>
                </div>
            );
        } else if (this.props.game.state === 'paused') {
            buttons = (
                <div>
                    <button className="btn btn-success stretch" onClick={this.props.resume}>
                        Resume Game
                    </button>
                </div>
            );
        } else {
            // game is playing live
            buttons = (
                <div>
                    <button className="btn btn-info stretch" onClick={this.props.pause}>
                        Pause Game
                    </button>
                </div>
            );
        }

        return (
            <div className="game-sidebar sidebar-inner">
                <h1>{this.props.gameId}</h1>
                <p>Turn {this.props.latestGameState ? this.props.latestGameState.turn : '--'}</p>

                <h2>Living Snakes</h2>
                {aliveSnakes}

                <h2>Dead Snakes</h2>
                {deadSnakes}

                <hr />

                {buttons}
            </div>
        );
    }
});


var GameListItem = React.createClass({
    render: function () {
        return (
            <div className="game-summary">

            </div>
        )
    }
});


var GameList = React.createClass({
    componentDidMount: function () {
        $.ajax({
            type: 'GET',
            url: '/api/games',
        }).done(function (response) {
            this.setState({ games: this.categorizeGames(response.data) });
        }.bind(this));
    },
    categorizeGames: function (gamesList) {
        var categories = { };

        for (var i = 0; i < gamesList.length; i++) {
            var game = gamesList[i];

            // Init the category if it isn't
            if (!categories[game.state]) {
                categories[game.state] = [];
            }

            categories[game.state].push(game);
        }
        return categories;
    },
    getInitialState: function () {
        return {
            games: this.categorizeGames(this.props.games || [])
        };
    },
    renderGameList: function (games) {
        return games.map(function (game, i) {
            var path = '/play/games/' + game._id
            return (
                <li key={game._id}><a href={path}>{game._id}</a></li>
            );
        });
    },
    render: function () {
        var playingGames = this.renderGameList(this.state.games.playing || [ ])
        var completedGames = this.renderGameList(this.state.games.done || [ ])

        return (
            <div>
                <h2>In Progress</h2>
                <ul>{playingGames}</ul>

                <h2>Finished Games</h2>
                <ul>{completedGames}</ul>
            </div>
        );
    }
});

var GameCreate = React.createClass({
    _loadPastState: function () {
        try {
            return JSON.parse(window.localStorage['battlesnake.new_game_state']);
        } catch (e) {
            return null;
        }
    },
    _savePastState: function () {
        var json = JSON.stringify(this.state);
        window.localStorage['battlesnake.new_game_state'] = json;
    },
    handleGameCreate: function (e) {
        e.preventDefault();

        var gameData = {
            snake_urls: this.state.snakeUrls,
            width: parseInt(this.state.currentWidth),
            height: parseInt(this.state.currentHeight),
            turn_time: parseFloat(this.state.currentTimeout),
        };

        this.setState({ isLoading: true });

        $.ajax({
            type: 'POST',
            url: '/api/games',
            data: JSON.stringify(gameData),
            contentType: 'application/json'
        }).done(function (response) {
            this._savePastState();
            this.setState({ isLoading: false });
            navigate('/play/games/' + response.data.game._id);
        }.bind(this)).error(function (xhr, textStatus, errorThrown) {
            alert(xhr.responseJSON.message);
            this.setState({ isLoading: false });
        }.bind(this));
    },
    handleSubmitSnake: function (e) {
        e.preventDefault();
        var snakeUrls = this.state.snakeUrls;
        snakeUrls.push(this.state.currentSnakeUrl);
        this.setState({ snakeUrls: snakeUrls, currentSnakeUrl: '' });
    },
    handleSnakeUrlChange: function (e) {
        this.setState({ currentSnakeUrl: e.target.value });
    },
    handleDeleteSnakeUrl: function (i, e) {
        var snakeUrls = this.state.snakeUrls;
        snakeUrls.splice(i, 1);
        this.setState({ snakeUrls: snakeUrls });
    },
    handleWidthChange: function (e) {
        this.setState({ currentWidth: e.target.value });
    },
    handleHeightChange: function (e) {
        this.setState({ currentHeight: e.target.value });
    },
    handleTimeoutChange: function (e) {
        this.setState({ currentTimeout: e.target.value });
    },
    getInitialState: function () {
        var state = this._loadPastState();
        if (state) {
            state.isLoading = false;
            return state;
        }

        return {
            snakeUrls: [ ],
            currentSnakeUrl: '',
            currentWidth: 20,
            currentHeight: 20,
            currentTimeout: 1,
            isLoading: false
        };
    },
    render: function () {
        var snakeUrls = this.state.snakeUrls.map(function (snakeUrl, i) {
            return (
                <div key={'url_' + i}>
                    <a href="#"
                        className="pull-right"
                        onClick={this.handleDeleteSnakeUrl.bind(null, i)}>
                        &times;
                    </a>
                    <p>{snakeUrl}</p>
                </div>
            );
        }.bind(this));

        var noSnakesMessage = '';
        if (!this.state.snakeUrls.length) {
            noSnakesMessage = (
                <p>You have no snake added. Input your snake url in the box below...</p>
            );
        }
        return (
            <div className="container">
                <form onSubmit={this.handleSubmitSnake}>
                    <h2>Create Game</h2>
                    <br />
                    {noSnakesMessage}
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
                    <div className="row">
                        <div className="col-md-4">
                            <label>width</label>
                            <input type="number"
                                className="form-control"
                                placeholder="width"
                                min="10"
                                max="50"
                                value={this.state.currentWidth}
                                onChange={this.handleWidthChange}/>
                        </div>
                        <div className="col-md-4">
                            <label>height</label>
                            <input type="number"
                                className="form-control"
                                placeholder="height"
                                min="10"
                                max="50"
                                value={this.state.currentHeight}
                                onChange={this.handleHeightChange}
                            />
                        </div>
                        <div className="col-md-4">
                            <label>turn time</label>
                            <input type="number"
                                step="0.1"
                                min="0.6"
                                className="form-control"
                                placeholder="1.0 (seconds)"
                                value={this.state.currentTimeout}
                                onChange={this.handleTimeoutChange}
                            />
                        </div>
                    </div>
                    <div className="input-group">
                        <button type="button" className="btn btn-big btn-success" onClick={this.handleGameCreate} disabled={this.state.isLoading}>
                            {this.state.isLoading ? 'Contacting snakes...' : 'Start Game'}
                        </button>
                    </div>
                </form>
            </div>
        );
    }
});

var GameOverModal = React.createClass({
    render: function () {
        if (!this.props.game || !this.props.latestGameState) {
            return <div></div>;
        }

        var winningSnake;

        if (this.props.latestGameState.snakes.length === 1) {
            winningSnake = this.props.latestGameState.snakes[0].name;
        } else {
            winningSnake = 'N/A';
        }

        return (
            <div className="modal fade" id="game-summary-modal" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <h4 className="modal-title">
                                Finished {this.props.game.id}
                            </h4>
                        </div>
                        <div className="modal-body">
                            Winner: {winningSnake}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-success" data-dismiss="modal">Continue</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});
