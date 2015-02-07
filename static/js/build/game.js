/** @jsx React.DOM */

var Game = React.createClass({displayName: "Game",
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
        board.init(this.state.latestGameState, function () { });
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
                    React.createElement("canvas", {ref: "canvas"}, "Your browser does not support canvas"), 
                    React.createElement("button", {onClick: this.handleClickNextTurn}, "Next")
                ), 
                React.createElement("div", {className: "col-md-3 sidebar"}, 
                    React.createElement(GameSidebar, {gameId: this.props.gameId})
                )
            )
        );
    }
});

var GameSidebar = React.createClass({displayName: "GameSidebar",
    render: function () {
        return (
            React.createElement("div", {className: "sidebar-inner"}, 
                React.createElement("h3", null, this.props.gameId), 
                React.createElement("ul", null, 
                	React.createElement("li", null, "Snake 1"), 
                	React.createElement("li", null, "Snake 2"), 
                	React.createElement("li", null, "Snake 3"), 
                	React.createElement("li", null, "Snake 4")
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
        games = this.state.games.map(function (game, i) {
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

