import React, { Component } from 'react';


export default class GameSidebarSnake extends Component {

  state = {
    lastTaunt: this.props.snake.taunt,
    tauntToShow: this.props.snake.taunt,
    tauntCount: 0
  }

  constructor (props) {
    super(props)

    this.handleTaunt(this.state, props);
  }

  componentWillReceiveProps (props) {
    let newState = this.handleTaunt(this.state, props);
    this.setState(newState);
  }

  componentDidMount () {
    let img = this.refs.head_img;
    img.onerror = () => {
      this.setAttribute('src', 'http://www.battlesnake.io/static/img/default_head.gif');
      this.onerror = undefined;
    }
  }

  handleTaunt (state, props) {
    let words = props.snake.taunt || state.lastTaunt;

    if (props.isDead) {
      words = 'Killed by ' + props.snake.killed_by;
    }

    if (words && words.length > 53) {
      words = words.substring(0, 50) + '...';
    }

    if (state.lastTaunt === words) {
      // Taunt is the same
      state.tauntCount++;
    } else {
      state.tauntCount = 0;
      state.lastTaunt = words;
    }

    if (state.tauntCount > 5) {
      state.tauntToShow = '';
    } else {
      state.tauntToShow = words;
    }

    return state;
  }

  render () {
    let snakeStyles = {
      backgroundColor: this.props.snake.color || 'red'
    };

    let tauntStyles = {
      display: this.state.tauntToShow ? 'block' : 'none',
      opacity: 1.3 - (this.state.tauntCount / 10)
    };

    if (!this.props.isDead) {
      tauntStyles.borderColor = this.props.snake.color;
    }

    let life = 100 - (this.props.turn - (this.props.snake.last_eaten || 0))

    if (this.props.isDead || life < 0) {
      life = 0;
    }

    let tauntClass = this.props.isDead ? 'dead' : 'alive';

    return (
      <div className="snake-block">
        <img src={this.props.snake.head_url} style={snakeStyles} ref='head_img' />
        <h3>{this.props.snake.name} <span className="muted">({this.props.snake.coords.length})</span></h3>
        <div className="meta">
          <div className="col">
            life: <strong>{life}</strong>
          </div>
          <div className="col">
            food: {this.props.snake.food_eaten || 0}
          </div>
          <div className="col">
            kills: {this.props.snake.kills || 0}
          </div>
        </div>
        <div className={'taunt ' + tauntClass} style={tauntStyles}>{this.state.tauntToShow}</div>
      </div>
    )
  }

}
