// Routing Setup
import React from 'react';
import { Router, Route, IndexRedirect } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

// Top-level components
import App from './app';

// Game Components
import GameCreate from './components/gameCreate';
import GameList from './components/gameList';
import GameListTournament from './components/gameListTournament';
import Game from './components/game';


const history = createBrowserHistory();

const router = () => {
  return (
    <Router history={history}>
      <Route path='/app' component={App}>
        <IndexRedirect from='/' to='games' />
        <Route path='games' component={GameList} />
        <Route path='games/tournament' component={GameListTournament} />
        <Route path='game/new' component={GameCreate} />
        <Route path='games/:id' component={Game} />
      </Route>
    </Router>
  );
}

export default router;
