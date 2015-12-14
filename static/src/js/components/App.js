class App extends React.Component {

  static mixins: [
    ReactMiniRouter.RouterMixin
  ]

  static routes = {
    '/': 'games',
    '/play': 'play',
    '/play/games': 'games',
    '/play/new': 'create',
    '/play/games/:gameId': 'game'
  }

  play () {
    window.location = '/play/games';
  }

  game (gameId) {
    return this.wrapPage(
      <Game gameId={gameId} />
    );
  }

  create () {
    return this.wrapPage(
      <GameCreate />
    );
  }

  games () {
    return this.wrapPage(
      <GameList />
    );
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

  render () {
    return this.renderCurrentRoute();
  }

}
