// Routing Setup
import React from 'react';
import { Router, Route, Redirect } from 'react-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

// Top-level components
import App from './app';

// Authentication / Authorization components


// Game Components
import GameCreate from './components/gameCreate';
import GameList from './components/gameList';
import Game from './components/game';

// Team Components


// Sign Up/ Sign In Components


// Analytics
import env from './config/environment';
// import ga from 'react-google-analytics';

// function runAnalytics() {
//   ga('create', env.gaId, 'auto');
//   ga('send', 'pageview');
// }

const history = createBrowserHistory();

// <Router history={history} onUpdate={runAnalytics}>
const router = () =>
  <Router history={history}>
    <Route path='/play' component={App}>
      <Route path='games' component={GameList} />
      <Route path='game/:id' component={Game} />
      <Route path='new' component={GameCreate} />
    </Route>
  </Router>

export default router;
