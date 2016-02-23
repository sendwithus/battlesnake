import React, { Component } from 'react';

import GameListItem from './gameListItem';
import getURLParameter from '../constants/getURLParameter';


export default class GameList extends Component {

  state = {
    games: this.categorizeGames(this.props.games || [])
  };

  componentDidMount () {
    $.ajax({
      type: 'GET',
      url: '/api/games/tournament'
    })
    .done((response) => {
      this.setState({ games: this.categorizeGames(response.data) });

      let loop = getURLParameter('loop');
      let lastGameId = getURLParameter('game_id');

      if (loop === 'true') {
        this.redirectToNextGame(response.data, lastGameId);
      }
    });
  }

  categorizeGames (gamesList) {
    let categories = {};

    for (var i = 0; i < gamesList.length; i++) {
      let game = gamesList[i];

      // Init the category if it isn't
      if (!categories[game.state]) {
        categories[game.state] = [];
      }

      categories[game.state].push(game);
    }

    return categories;
  }

  redirectToNextGame (gamesList, gameId) {
    let foundGame = false;
    let nextGame;

    for (var i = 0; i < gamesList.length; i++) {
      let game = gamesList[i];

      if(foundGame) {
        nextGame = game;
        break;
      }

      if (game._id === gameId) {
        foundGame = true;
      }
    }

    if (!nextGame) {
      // loop around to first game
      nextGame = gamesList[0];
    }

    window.location = '/app/games/' + nextGame._id + '?loop=true';
  }

  renderGameList (games) {
    return games.map((game, i) => {
      return (
        <GameListItem key={game._id} game={game} />
      );
    });
  }

  render () {
    let playingGames = this.renderGameList(this.state.games.playing || [ ])
    let completedGames = this.renderGameList(this.state.games.done || [ ])

    let noGamesMessage = <span></span>;

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

}
