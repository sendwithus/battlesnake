import React from 'react';
import ReactDOM from 'react-dom';
import Router from './router';

/* renderApp is called outside of the app itself, dependant on AJAX call completing */
window.app.render = () => {
  ReactDOM.render(
    <Router />,
    document.getElementById('root')
  );
}
