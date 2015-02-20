/** @jsx React.DOM */

var navigate = ReactMiniRouter.navigate;

var Game = React.createClass({displayName: "Game",
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
            React.createElement("div", {className: "row"}, 
                React.createElement("div", {className: "col-md-9"}, 
                    React.createElement("canvas", {ref: "canvas"}, "Your browser does not support canvas")
                ), 
                React.createElement("div", {className: "col-md-3 sidebar"}, 
                    React.createElement(GameSidebar, {
                        gameId: this.props.gameId, 
                        game: this.state.game, 
                        isReplay: this.state.isReplay, 
                        isLoading: this.state.isLoading, 
                        latestGameState: this.state.latestGameState, 
                        continueous: this.handleClickContinuous, 
                        startAutomated: this.handleStart.bind(null, false), 
                        startManual: this.handleStart.bind(null, true), 
                        startReplay: this.handleReplay, 
                        cancelReplay: this.handleCancelReplay, 
                        pause: this.handlePause, 
                        resume: this.handleResume, 
                        nextTurn: this.handleClickNextTurn})
                ), 
                React.createElement(GameOverModal, {
                    game: this.state.game, 
                    latestGameState: this.state.latestGameState}
                )
            )
        );
    }
});

var GameSidebarSnake = React.createClass({displayName: "GameSidebarSnake",
    render: function () {
        var snakeStyles = {
            backgroundColor: this.props.snake.color || 'red'
        };

        return (
            React.createElement("div", {className: "snake-block"}, 
                React.createElement("img", {src: this.props.snake.head_url, style: snakeStyles}), 
                React.createElement("h3", null, this.props.snake.name), 
                React.createElement("div", {className: "row meta"}, 
                    React.createElement("div", {className: "col-md-3"}, 
                        "score: ", this.props.snake.coords.length
                    ), 
                    React.createElement("div", {className: "col-md-3"}, 
                        "score: ", this.props.snake.coords.length
                    ), 
                    React.createElement("div", {className: "col-md-3"}, 
                        "score: ", this.props.snake.coords.length
                    )
                )
            )
        )
    }
});

var GameSidebar = React.createClass({displayName: "GameSidebar",
    render: function () {
        var snakes = '';

        if (!this.props.latestGameState) {
            return React.createElement("div", null);
        }

        var aliveSnakes = this.props.latestGameState.snakes.map(function (snake, i) {
            return React.createElement(GameSidebarSnake, {key: 'a_' + i, snake: snake})
        });

        var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
            return React.createElement(GameSidebarSnake, {key: 'd_' + i, snake: snake})
        });

        if (!deadSnakes.length) {
            deadSnakes = React.createElement("p", null, "None Yet");
        }


        var buttons;

        if (!this.props.game) {
            buttons = ('');
        } else if (this.props.game.state === 'created') {
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.startAutomated}, 
                        "Start Automated"
                    ), 
                    React.createElement("br", null), 
                    React.createElement("br", null), 
                    React.createElement("button", {className: "btn btn-info stretch", onClick: this.props.startManual}, 
                        "Start Debug (Step Through)"
                    )
                )
            );
        } else if (this.props.game.state === 'manual') {
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.nextTurn, disabled: this.props.isLoading}, 
                        this.props.isLoading ? '...' : 'Play Turn ' + (this.props.latestGameState.turn + 1)
                    )
                )
            );
        } else if (!this.props.isReplay && this.props.game.state === 'done') {
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.startReplay}, 
                        "View Replay"
                    )
                )
            );
        } else if (this.props.isReplay && this.props.game.state === 'done') {
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-info stretch", onClick: this.props.cancelReplay}, 
                        "Cancel Replay"
                    )
                )
            );
        } else if (this.props.game.state === 'paused') {
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.resume}, 
                        "Resume Game"
                    )
                )
            );
        } else {
            // game is playing live
            buttons = (
                React.createElement("div", null, 
                    React.createElement("button", {className: "btn btn-info stretch", onClick: this.props.pause}, 
                        "Pause Game"
                    )
                )
            );
        }

        return (
            React.createElement("div", {className: "game-sidebar sidebar-inner"}, 
                React.createElement("h1", null, this.props.gameId), 
                React.createElement("p", null, "Turn ", this.props.latestGameState ? this.props.latestGameState.turn : '--'), 

                React.createElement("h2", null, "Living Snakes"), 
                aliveSnakes, 

                React.createElement("h2", null, "Dead Snakes"), 
                deadSnakes, 

                React.createElement("hr", null), 

                buttons
            )
        );
    }
});


// var GameListItem = React.createClass({
// });


var GameList = React.createClass({displayName: "GameList",
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
                React.createElement("li", {key: game._id}, React.createElement("a", {href: path}, game._id))
            );
        });
    },
    render: function () {
        var playingGames = this.renderGameList(this.state.games.playing || [ ])
        var completedGames = this.renderGameList(this.state.games.done || [ ])

        return (
            React.createElement("div", null, 
                React.createElement("h2", null, "In Progress"), 
                React.createElement("ul", null, playingGames), 

                React.createElement("h2", null, "Finished Games"), 
                React.createElement("ul", null, completedGames)
            )
        );
    }
});

var GameCreate = React.createClass({displayName: "GameCreate",
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
                React.createElement("div", {key: 'url_' + i}, 
                    React.createElement("a", {href: "#", 
                        className: "pull-right", 
                        onClick: this.handleDeleteSnakeUrl.bind(null, i)}, 
                        "×"
                    ), 
                    React.createElement("p", null, snakeUrl)
                )
            );
        }.bind(this));

        var noSnakesMessage = '';
        if (!this.state.snakeUrls.length) {
            noSnakesMessage = (
                React.createElement("p", null, "You have no snake added. Input your snake url in the box below...")
            );
        }
        return (
            React.createElement("div", {className: "container"}, 
                React.createElement("form", {onSubmit: this.handleSubmitSnake}, 
                    React.createElement("h2", null, "Create Game"), 
                    React.createElement("br", null), 
                    noSnakesMessage, 
                    React.createElement("div", null, 
                        snakeUrls
                    ), 
                    React.createElement("div", {className: "input-group"}, 
                        React.createElement("input", {type: "text", 
                            className: "form-control", 
                            value: this.state.currentSnakeUrl, 
                            name: "snake-url", 
                            placeholder: "http://mysnake.herokuapp.com", 
                            onChange: this.handleSnakeUrlChange}
                        ), 
                        React.createElement("span", {className: "input-group-btn"}, 
                            React.createElement("button", {type: "submit", 
                                    disabled: this.state.currentSnakeUrl ? false : 'on', 
                                    className: "btn btn-info big form-control"}, 
                                "Add Snake"
                            )
                        )
                    ), 
                    React.createElement("div", {className: "row"}, 
                        React.createElement("div", {className: "col-md-4"}, 
                            React.createElement("label", null, "width"), 
                            React.createElement("input", {type: "number", 
                                className: "form-control", 
                                placeholder: "width", 
                                min: "10", 
                                max: "50", 
                                value: this.state.currentWidth, 
                                onChange: this.handleWidthChange})
                        ), 
                        React.createElement("div", {className: "col-md-4"}, 
                            React.createElement("label", null, "height"), 
                            React.createElement("input", {type: "number", 
                                className: "form-control", 
                                placeholder: "height", 
                                min: "10", 
                                max: "50", 
                                value: this.state.currentHeight, 
                                onChange: this.handleHeightChange}
                            )
                        ), 
                        React.createElement("div", {className: "col-md-4"}, 
                            React.createElement("label", null, "turn time"), 
                            React.createElement("input", {type: "number", 
                                step: "0.1", 
                                min: "0.6", 
                                className: "form-control", 
                                placeholder: "1.0 (seconds)", 
                                value: this.state.currentTimeout, 
                                onChange: this.handleTimeoutChange}
                            )
                        )
                    ), 
                    React.createElement("div", {className: "input-group"}, 
                        React.createElement("button", {type: "button", className: "btn btn-big btn-success", onClick: this.handleGameCreate, disabled: this.state.isLoading}, 
                            this.state.isLoading ? 'Contacting snakes...' : 'Start Game'
                        )
                    )
                )
            )
        );
    }
});

var GameOverModal = React.createClass({displayName: "GameOverModal",
    render: function () {
        if (!this.props.game || !this.props.latestGameState) {
            return React.createElement("div", null);
        }

        var winningSnake;

        if (this.props.latestGameState.snakes.length === 1) {
            winningSnake = this.props.latestGameState.snakes[0].name;
        } else {
            winningSnake = 'N/A';
        }

        return (
            React.createElement("div", {className: "modal fade", id: "game-summary-modal", tabIndex: "-1", role: "dialog", "aria-labelledby": "myModalLabel", "aria-hidden": "true"}, 
                React.createElement("div", {className: "modal-dialog"}, 
                    React.createElement("div", {className: "modal-content"}, 
                        React.createElement("div", {className: "modal-header"}, 
                            React.createElement("button", {type: "button", className: "close", "data-dismiss": "modal", "aria-label": "Close"}, React.createElement("span", {"aria-hidden": "true"}, "×")), 
                            React.createElement("h4", {className: "modal-title"}, 
                                "Finished ", this.props.game.id
                            )
                        ), 
                        React.createElement("div", {className: "modal-body"}, 
                            "Winner: ", winningSnake
                        ), 
                        React.createElement("div", {className: "modal-footer"}, 
                            React.createElement("button", {type: "button", className: "btn btn-success", "data-dismiss": "modal"}, "Continue")
                        )
                    )
                )
            )
        );
    }
});
