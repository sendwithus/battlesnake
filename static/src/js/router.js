// Routing Setup
import React from 'react';
import { Router, Route, IndexRedirect } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

// Top-level components
import App from './app';

// Game Components
import GameCreate from './components/gameCreate';
import GameList from './components/gameList';
import Game from './components/game';


const history = createBrowserHistory();

const router = () => {
  return (
    <Router history={history}>
      <Route path='/app' component={App}>
        <IndexRedirect from='/' to='games' />
        <Route path='games' component={GameList} />
        <Route path='games/:id' component={Game} />
        <Route path='game/new' component={GameCreate} />
      </Route>
    </Router>
  );
}

export default router;
