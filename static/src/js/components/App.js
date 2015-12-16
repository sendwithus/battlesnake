import RouterMixin from "react-mini-router";


class App extends React.Component {

  constructor () {
    super()

    this.mixins = [
      RouterMixin
    ]

    this.routes = {
      '/': 'games',
      '/play': 'play',
      '/play/games': 'games',
      '/play/new': 'create',
      '/play/games/:gameId': 'game'
    }
  }

  render () {
    return this.renderCurrentRoute();
  }

  wrapPage (page) {
    return (
      <div>
        <Navbar />
        <div className="container-fluid">
          {page}
        </div>
      </div>
    );
  }

  play () {
    window.location = '/play/games';
  }

  create () {
    return this.wrapPage(
      <GameCreate />
    );
  }

  game (gameId) {
    return this.wrapPage(
      <Game gameId={gameId} />
    );
  }

  games () {
    return this.wrapPage(
      <GameList />
    );
  }

}
