import React from 'react';
import navigate from 'react-router';


export default class GameList extends React.Component {
  state = {
    games: this.categorizeGames(this.props.games || [])
  }

  componentDidMount () {
    $.ajax({ url: '/api/games' })
    .done((response) => {
      this.setState({ games: this.categorizeGames(response.data) });
    });
  }

  categorizeGames (gamesList) {
    let categories = {};

    for (var game of gamesList) {
      // Init the category if it isn't
      if (!categories[game.state]) {
        categories[game.state] = [];
      }

      categories[game.state].push(game);
    }
    return categories;
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
