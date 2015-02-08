/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
    handleClickNextTurn: function () {
        $.ajax({
            type: 'POST',
            url: '/api/games/' + this.props.gameId + '/turn'
        }).done(function (response) {
            // console.log('Got GameState', response.data);
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
            React.createElement("div", {className: "row"}, 
                React.createElement("div", {className: "col-md-9"}, 
                    React.createElement("canvas", {ref: "canvas"}, "Your browser does not support canvas")
                ), 
                React.createElement("div", {className: "col-md-3 sidebar"}, 
                    React.createElement(GameSidebar, {
                        gameId: this.props.gameId, 
                        latestGameState: this.state.latestGameState, 
                        continueous: this.handleClickContinuous, 
                        nextTurn: this.handleClickNextTurn})
                )
            )
        );
    }
});

var GameSidebar = React.createClass({displayName: "GameSidebar",
    render: function () {
        var snakes = '';

        if (this.props.latestGameState) {
            var snakes = this.props.latestGameState.snakes.map(function (snake, i) {
                return React.createElement("li", {key: snake.snake_id}, snake.name, " (", snake.coords.length, ")");
            });
            var deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
                return React.createElement("li", {key: snake.snake_id}, snake.name, " (", snake.coords.length, ")");
            });
        }

        return (
            React.createElement("div", {className: "game-sidebar sidebar-inner"}, 
                React.createElement("h3", null, this.props.gameId), 
                React.createElement("ul", null, snakes), 
                React.createElement("ul", null, deadSnakes), 
                React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.nextTurn}, 
                    "Next Turn"
                ), 
                React.createElement("br", null), 
                React.createElement("br", null), 
                React.createElement("button", {className: "btn btn-success stretch", onClick: this.props.continueous}, 
                    "Continueous"
                )
            )
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
        var games = this.state.games.map(function (game, i) {
            var path = '/play/watch/' + game._id
            return (
                React.createElement("li", {key: game._id}, React.createElement("a", {href: path}, game._id))
            );
        });

        return (
            React.createElement("div", null, 
                React.createElement("h2", null, "Current Games"), 
                React.createElement("ul", null, games)
            )
        );
    }
});

var GameCreate = React.createClass({displayName: "GameCreate",
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
                React.createElement("div", {className: "form-group", key: i}, 
                    React.createElement("input", {type: "text", 
                        className: "form-control", 
                        value: this.state.snakeUrls[i], 
                        placeholder: "http://my-snake-url.com/api", 
                        onChange: this.handleSnakeUrlChange.bind(this, i)})
                )
            );
        }.bind(this));

        return (
            React.createElement("form", {onSubmit: this.handleGameCreate}, 
                React.createElement("h3", null, "New Game"), 
                snakeUrls, 
                React.createElement("div", {className: "form-group"}, 
                    React.createElement("button", {type: "button", 
                        onClick: this.handleAddSnakeUrl, 
                        className: "btn btn-info form-control"}, "Add Snake")
                ), 
                React.createElement("div", {className: "form-group"}, 
                    React.createElement("button", {type: "submit", className: "btn btn-success form-control"}, 
                        "Create Game"
                    )
                )
            )
        );
    }
});

