import React, { Component } from 'react';
import { Link } from 'react-router';

const MAX_SNAKES = 12

export default class GameListItem extends Component {

  render () {
    let gamePath = '/app/games/' + this.props.game._id

    let body = <div className="pull-left"></div>
    let rematchBtn = ''
    let snakes = []
    
    if (this.props.game.state === 'done') {
      snakes = this.props.game.stats.snakes.sort((a, b) => {
        if(a.name < b.name) { return -1 }
        if(a.name > b.name) { return 1 }
        return 0
      })
    } else {
      snakes = this.props.game.snakes.sort((a, b) => {
        if(a.name < b.name) { return -1 }
        if(a.name > b.name) { return 1 }
        return 0
      })
    }

    let snakeImages = snakes.map((snake, i) => {
      let snakeStyles = {
        backgroundColor: snake.color
      }

      let deathMessage;
      if (snake.status == "dead") {
        deathMessage = snake.killed_by + ' on turn ' + snake.age;
      } else {
        deathMessage= 'n/a';
      }

      let classNames = 'game-summary-snake'
      if (snake.name === this.props.game.stats.winner) {
        classNames += ' game-summary-snake-winner'
      }

      return (
        <div className={classNames} key={i + '-' +this.props.game._id  + '-' + snake.name}>
          <img src={snake.head} style={snakeStyles} title={snake.name} />
        </div>
      )
    })

    // Build the list of snakes in a finished game
    do {
      snakeImages.push(
        <div className="game-summary-snake" key={snakeImages.length}></div>
      )
    } while (snakeImages.length < MAX_SNAKES)

    body = snakeImages

    // Build the snakes to be used in a rematch
    let rematchTeams = []
    if (this.props.game.state === 'done') {
      let teams = this.props.game.teams
      for (let team of teams) {
        rematchTeams.push(team)
      }
    }

    if (this.props.game.state === 'done') {
      rematchBtn = (
        <Link to='/app/game/new'
              state={{ rematchTeams: rematchTeams }}
              className="btn btn-success btn-lg pull-right">
            Rematch
        </Link>
      )
    }

    return (
      <table className="table table-bordered game-summary">
        <tbody>
          <tr>
            <td>
              <div className="pull-left">
                {body}
              </div>
              <div className="game-summary-buttons pull-right">
                {rematchBtn}
                <Link to={gamePath}
                      className="btn btn-primary btn-lg pull-right"
                      style={{ verticalAlign: 'middle' }}>
                    {this.props.game.state === 'done' ? 'Watch Replay' : 'View Live'}
                </Link>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    )
  }

}
