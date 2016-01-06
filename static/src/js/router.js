// Routing Setup
import React from 'react';
import { Router, Route } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

// Top-level components
import App from './app';

// Game Components
import GameCreate from './components/gameCreate';
import GameList from './components/gameList';
import Game from './components/game';

// Team Components
// to be completed?

const history = createBrowserHistory();

const router = () =>
  <Router history={history}>
    <Route path='/play' component={App}>
      <Route path='games' component={GameList} />
      <Route path='games/:id' component={Game} />
      <Route path='new' component={GameCreate} />
    </Route>
  </Router>

export default router;
