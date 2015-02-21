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

        if (!this.board) {
            this.board = this.getBoard();
            this.board.init(this.state.game.width, this.state.game.height);
        }

        this.board.update(this.state.latestGameState );
    },
    getBoard: function () {
        var canvas = this.refs.canvas.getDOMNode();
        var ctx = canvas.getContext('2d');
        return new Board(ctx, canvas);
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
        var state = {
            lastTaunt: this.props.snake.taunt,
            tauntToShow: this.props.snake.taunt,
            tauntCount: 0
        };

        return this.handleTaunt(state, this.props);
    },
    componentWillReceiveProps: function (nextProps) {
        var newState = this.handleTaunt(this.state, nextProps);
        this.setState(newState);
    },
    componentDidMount: function () {
        var img = this.refs.head_img.getDOMNode();
        img.onerror = function () {
            this.setAttribute('src', 'http://www.battlesnake.io/static/img/default_head.gif');
            this.onerror = undefined;
        }
    },
    handleTaunt: function (state, props) {
        var words = props.snake.taunt || state.lastTaunt;

        if (props.isDead) {
            words = 'Killed by ' + props.snake.killed_by;
        }

        if (words && words.length > 53) {
            words = words.substring(0, 50) + '...';
        }

        if (state.lastTaunt === words) {
            // Taunt is the same
            state.tauntCount++;
        } else {
            state.tauntCount = 0;
            state.lastTaunt = words;
        }

        if (state.tauntCount > 5) {
            state.tauntToShow = '';
        } else {
            state.tauntToShow = words;
        }

        return state;
    },
    render: function () {
        var snakeStyles = {
            backgroundColor: this.props.snake.color || 'red'
        };

        var tauntStyles = {
            display: this.state.tauntToShow ? 'block' : 'none',
            opacity: 1.3 - (this.state.tauntCount / 10),
            borderColor: this.props.isDead ? '#9e0000' : '#ABA700'
        };

        var life = 101 - (this.props.turn - (this.props.snake.last_eaten || 0))

        if (life < 0) {
            life = 0;
        }

        return (
            <div className="snake-block">
                <img src={this.props.snake.head_url} style={snakeStyles} ref='head_img' />
                <h3>{this.props.snake.name} <span className="muted">({this.props.snake.coords.length})</span></h3>
                <div className="meta">
                    <div className="col">
                        life: <strong>{life}</strong>
                    </div>
                    <div className="col">
                        food: {this.props.snake.food_eaten || 0}
                    </div>
                    <div className="col">
                        kills: {this.props.snake.kills || 0}
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
            return <GameSidebarSnake key={snake.name} snake={snake} isDead={false} turn={this.props.latestGameState.turn} />
        }.bind(this));

        var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
            return <GameSidebarSnake key={snake.name} snake={snake} isDead={true} turn={this.props.latestGameState.turn} />
        }.bind(this));

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
        var path = '/play/games/' + this.props.game._id
        var tdStyles = { width: '25%' };
        var tbody = <tr></tr>;

        if (this.props.game.state === 'done') {
            var snakeHeader = (
                <tr className="snakes-heading">
                    <td>Snake Stats</td>
                    <td>length</td>
                    <td>food</td>
                    <td>kills</td>
                </tr>
            );
            var snakeRows = this.props.game.stats.snakes.map(function (snake, i) {
                return (
                    <tr key={this.props.game.id + snake.name}>
                        <td>{snake.name}</td>
                        <td className="text-center">{snake.coords.length}</td>
                        <td className="text-center">{snake.food_eaten || 0}</td>
                        <td className="text-center">{snake.kills || 0}</td>
                    </tr>
                )
            }.bind(this));

            tbody = (
                <tbody>
                    <tr>
                        <td style={tdStyles}>
                            <h4>Winner</h4>
                            <p>{this.props.game.stats.winner || '--'}</p>
                        </td>
                        <td style={tdStyles}>
                            <h4>Hungriest</h4>
                            <p>{this.props.game.stats.hungriest || '--'}</p>
                        </td>
                        <td style={tdStyles}>
                            <h4>Deadliest</h4>
                            <p>{this.props.game.stats.deadliest || '--'}</p>
                        </td>
                        <td style={tdStyles}>
                            <h4>Longest</h4>
                            <p>{this.props.game.stats.longest || '--'}</p>
                        </td>
                    </tr>
                    {snakeHeader}
                    {snakeRows}
                </tbody>
            );
        }

        var watchLink;
        if (this.props.game.state === 'done') {
            watchLink = <a href={path} className="btn btn-info pull-right">Watch Replay</a>
        } else {
            watchLink = <a href={path} className="btn btn-success pull-right">View Live</a>
        }

        return (
            <table className="table table-bordered game-summary">
                <thead>
                    <tr>
                        <th colSpan="4">
                            {watchLink}
                            <h1><a href={path}>{this.props.game._id}</a></h1>
                        </th>
                    </tr>
                </thead>
                {tbody}
            </table>
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
            return (
                <GameListItem key={game._id} game={game} />
            );
        });
    },
    render: function () {
        var playingGames = this.renderGameList(this.state.games.playing || [ ])
        var completedGames = this.renderGameList(this.state.games.done || [ ])

        var noGamesMessage = <span></span>;

        if (!playingGames.length) {
            playingGames = <p>No games in progress</p>;
        }

        return (
            <div>
                <br />
                <h2>In Progress</h2>
                <div className="games-list playing-games">
                    {playingGames}
                </div>

                <br />
                <br />
                <h2>Finished Games</h2>
                <div className="games-list finished-games">
                    {completedGames}
                </div>
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
        var snakeUrl  = this.state.currentSnakeUrl;
        var snakeUrls = this.state.snakeUrls;
        if (!snakeUrl.match(/^[a-zA-Z]+:\/\//)) {
            snakeUrl = 'http://' + snakeUrl;
        }
        if(snakeUrl.substr(-1) === '/') {
            snakeUrl = snakeUrl.substr(0, snakeUrl.length - 1);
        }
        snakeUrls.push(snakeUrl.toLowerCase());
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
