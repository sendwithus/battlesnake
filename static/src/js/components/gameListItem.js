import React, { Component } from 'react';


export default class GameListItem extends Component {

  render () {
    let path = '/app/games/' + this.props.game._id
    let tdStyles = { width: '20%' };
    let tbody = <tbody><tr></tr></tbody>;

    if (this.props.game.state === 'done') {
      let snakeHeader = (
        <tr className="snakes-heading">
          <td>Snake Stats</td>
          <td>length</td>
          <td>food</td>
          <td>kills</td>
          <td>killed by...</td>
        </tr>
      );

      let snakeRows = this.props.game.stats.snakes.map((snake, i) => {
        let snakeStyles = {
          backgroundColor: snake.color
        };

        let deathMessage;
        if (snake.died_on_turn) {
          deathMessage = snake.killed_by + ' on turn ' + snake.died_on_turn;
        } else {
          deathMessage= 'n/a';
        }

        return (
          <tr key={this.props.game.id + snake.name}>
            <td className="snake-name">
              <img src={snake.head} style={snakeStyles} />
              <div className="name">
                {snake.name}
              </div>
              <div className="url muted">
                {snake.url}
              </div>
            </td>
            <td className="text-center stat">{snake.coords.length}</td>
            <td className="text-center stat">{snake.food_eaten || 0}</td>
            <td className="text-center stat">{snake.kills || 0}</td>
            <td className="text-center stat">{deathMessage}</td>
          </tr>
        )
      });

      tbody = (
        <tbody>
          <tr>
            <td style={tdStyles}>
              <h4>Winner</h4>
              <p>{this.props.game.stats.winner || '--'}</p>
            </td>
            <td style={tdStyles}>
              <h4>Longest</h4>
              <p>{this.props.game.stats.longest || '--'}</p>
            </td>
            <td style={tdStyles}>
              <h4>Hungriest</h4>
              <p>{this.props.game.stats.hungriest || '--'}</p>
            </td>
            <td style={tdStyles}>
              <h4>Deadliest</h4>
              <p>{this.props.game.stats.deadliest || '--'}</p>
            </td>
            <td style={tdStyles}>
            </td>
          </tr>
          {snakeHeader}
          {snakeRows}
        </tbody>
      );
    }

    let watchLink;
    if (this.props.game.state === 'done') {
      watchLink = <a href={path} className="btn btn-primary pull-right">Watch Replay</a>
    } else {
      watchLink = <a href={path} className="btn btn-primary pull-right">View Live</a>
    }

    return (
      <table className="table table-bordered game-summary">
        <thead>
          <tr>
            <th colSpan="5">
              {watchLink}
              <h1>
                <a href={path}>{this.props.game._id}</a>
                <span className="muted small">
                  {this.props.game.width} &times; {this.props.game.height}
                </span>
              </h1>
            </th>
          </tr>
        </thead>
        {tbody}
      </table>
    )
  }

}
