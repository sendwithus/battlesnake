import React, { Component } from 'react';

import GameSidebarSnake from './gameSidebarSnake'


export default class GameSidebar extends Component {

  render () {
    if (!this.props.latestGameState) {
      return (
        <div></div>
      );
    }

    let buttons;
    let aliveSnakes = this.props.latestGameState.snakes
    let deadSnakes = this.props.latestGameState.dead_snakes
    let allSnakes = aliveSnakes.concat(deadSnakes)

    let snakes = allSnakes.map((snake, i) => {
      return (
        <GameSidebarSnake
          key={snake.name}
          snake={snake}
          isDead={snake.status !== "alive"}
          turn={this.props.latestGameState.turn}
          showGold={this.props.latestGameState.mode === 'advanced'}
        />
      )
    });

    if (!this.props.game) {
      buttons = ('');
    } else if (this.props.game.state === 'created') {
      buttons = (
        <div>
          <button className="btn btn-success btn-block" onClick={this.props.startAutomated}>
            Start Automated
          </button>
          <br />
          <br />
          <button className="btn btn-info btn-block" onClick={this.props.startManual}>
            Start Debug (Step Through)
          </button>
        </div>
      );
    } else if (this.props.game.state === 'manual') {
      buttons = (
        <div>
          <button className="btn btn-success btn-block" onClick={this.props.nextTurn} disabled={this.props.isLoading}>
            {this.props.isLoading ? '...' : 'Play Turn ' + (this.props.latestGameState.turn + 1)}
          </button>
        </div>
      );
    } else if (this.props.game.state === 'done') {
      if (!this.props.isReplay) {
        buttons = (
          <div>
            <button className="btn btn-success btn-block" onClick={this.props.startReplay}>
              View Replay
            </button>
            <br />
            <br />
            <button className="btn btn-info btn-block" onClick={this.props.rematch}>
              Rematch
            </button>
          </div>
        );
      } else {
        buttons = (
          <div>
            <button className="btn btn-info btn-block" onClick={this.props.cancelReplay}>
              Cancel Replay
            </button>
          </div>
        );
      }
    } else if (this.props.game.state === 'paused') {
        buttons = (
          <div>
            <button className="btn btn-success btn-block" onClick={this.props.resume}>
              Resume Game
            </button>
          </div>
        );
    } else {
        // game is playing live
        buttons = (
          <div>
            <button className="btn btn-info btn-block" onClick={this.props.pause}>
              Pause Game
            </button>
          </div>
        );
    }

    return (
      <div className="game-sidebar sidebar-inner">
        <h1>{this.props.game._id}</h1>
        <h3>Mode: {this.props.game.mode}</h3>
        <p>Turn {this.props.latestGameState ? this.props.latestGameState.turn : '--'}</p>
        {snakes}
        <hr />
        {buttons}
      </div>
    );
  }

}
