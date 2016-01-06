// import React from 'react';
// import RouterMixin from 'react-router';
// import Navbar from './navbar';
// import Game from './game';
// import GameCreate from './game-create';
//
//
// export default class AppComponent extends React.Component {
//
//   constructor () {
//     super()
//
//     this.mixins = [
//       RouterMixin
//     ]
//
//     this.routes = {
//       '/': 'games',
//       '/play': 'play',
//       '/play/games': 'games',
//       '/play/new': 'create',
//       '/play/games/:gameId': 'game'
//     }
//   }
//
//   render () {
//     return this.renderCurrentRoute();
//   }
//
//   wrapPage (page) {
//     return (
//       <div>
//         <Navbar />
//         <div className="container-fluid">
//           {page}
//         </div>
//       </div>
//     );
//   }
//
//   play () {
//     window.location = '/play/games';
//   }
//
//   create () {
//     return this.wrapPage(
//       <GameCreate />
//     );
//   }
//
//   game (gameId) {
//     return this.wrapPage(
//       <Game gameId={gameId} />
//     );
//   }
//
//   games () {
//     return this.wrapPage(
//       <GameList />
//     );
//   }
//
// }
