import React from 'react';


export default class GameSidebar extends React.Component {

  render () {
    let buttons;
    let snakes = '';

    if (!this.props.latestGameState) {
      return <div></div>;
    }

    let aliveSnakes = this.props.latestGameState.snakes.map(function (snake, i) {
      return <GameSidebarSnake key={snake.name} snake={snake} isDead={false} turn={this.props.latestGameState.turn} />
    });

    let deadSnakes = this.props.latestGameState.dead_snakes.map(function (snake, i) {
      return <GameSidebarSnake key={snake.name} snake={snake} isDead={true} turn={this.props.latestGameState.turn} />
    });

    if (!deadSnakes.length) {
      deadSnakes = <p>None Yet</p>;
    }

    if (!this.props.game) {
      buttons = ('');
    } else if (this.props.game.state === 'created') {
      buttons = (
        <div>
          <button className="btn btn-success stretch" onClick={this.props.startAutomated}>
            Start Automated
          </button>
          <br />
          <br />
          <button className="btn btn-info stretch" onClick={this.props.startManual}>
            Start Debug (Step Through)
          </button>
        </div>
      );
    } else if (this.props.game.state === 'manual') {
      buttons = (
        <div>
          <button className="btn btn-success stretch" onClick={this.props.nextTurn} disabled={this.props.isLoading}>
            {this.props.isLoading ? '...' : 'Play Turn ' + (this.props.latestGameState.turn + 1)}
          </button>
        </div>
      );
    } else if (!this.props.isReplay && this.props.game.state === 'done') {
        buttons = (
          <div>
            <button className="btn btn-success stretch" onClick={this.props.startReplay}>
              View Replay
            </button>
            <br />
            <br />
            <button className="btn btn-info stretch" onClick={this.props.rematch}>
              Rematch
            </button>
          </div>
        );
    } else if (this.props.isReplay && this.props.game.state === 'done') {
        buttons = (
          <div>
            <button className="btn btn-info stretch" onClick={this.props.cancelReplay}>
              Cancel Replay
            </button>
          </div>
        );
    } else if (this.props.game.state === 'paused') {
        buttons = (
          <div>
            <button className="btn btn-success stretch" onClick={this.props.resume}>
              Resume Game
            </button>
          </div>
        );
    } else {
        // game is playing live
        buttons = (
          <div>
            <button className="btn btn-info stretch" onClick={this.props.pause}>
              Pause Game
            </button>
          </div>
        );
    }

    return (
      <div className="game-sidebar sidebar-inner">
        <h1>{this.props.gameId}</h1>
        <p>Turn {this.props.latestGameState ? this.props.latestGameState.turn : '--'}</p>

        <h2>Living Snakes</h2>
        {aliveSnakes}

        <h2>Dead Snakes</h2>
        {deadSnakes}

        <hr />

        {buttons}
      </div>
    );
  }

}
