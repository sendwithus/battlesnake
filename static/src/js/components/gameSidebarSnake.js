import React, { Component } from 'react';

export default class GameSidebarSnake extends Component {

  state = {
    lastTaunt: this.props.snake.taunt,
    tauntToShow: this.props.snake.taunt,
    tauntCount: 0
  };

  constructor (props) {
    super(props)

    this.handleTaunt(this.state, props);
  }

  componentWillReceiveProps (props) {
    let newState = this.handleTaunt(this.state, props);
    this.setState(newState);
  }

  componentDidMount () {
    let img = this.refs.head;
    img.onerror = () => {
      img.setAttribute('src', `${window.location.origin}/static/img/default_head.gif`);
      this.onerror = undefined;
    }
  }

  handleTaunt (state, props) {
    let words = props.snake.taunt || state.lastTaunt;
    let deathMessage = 'Killed by ' + props.snake.killed_by

    if (props.isDead) {
      words = deathMessage;
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

    if (props.isDead) {
      state.tauntToShow = deathMessage;
    }

    return state;
  }

  render () {
    let snakeStyles = {
      backgroundColor: this.props.snake.color || 'red'
    };

    let tauntStyles = {
      display: this.state.tauntToShow || this.props.isDead ? 'block' : 'none',
      opacity: this.props.isDead ? 1 : 1.3 - (this.state.tauntCount / 10)
    };

    if (!this.props.isDead) {
      tauntStyles.borderColor = this.props.snake.color;
    }

    let tauntClass = this.props.isDead ? 'dead' : 'alive';

    var goldIndicator = [];

    if (this.props.showGold) {
      let i = 0;
      _.times(this.props.snake.gold || 0, function() {
        goldIndicator.push(
          <div key={i++} className="gold-coin">
            <img src='/static/img/img-coin.gif' style={{borderRadius: '100%', width: '30px', height: '30px'}} />
          </div>
        );
      })
    }

    var healthScale = d3.scale.linear().domain([0,50,100]).range(['red', 'orange', 'green']);

    return (
      <div className="snake-block">
        <img src={this.props.snake.head} style={snakeStyles} ref='head' />
        <h3 className="snake-team-name">{this.props.snake.name} <span className="muted">({this.props.snake.coords.length})</span></h3>
        <div className="health-bar">
          <div className="inner" style={{width: this.props.snake.health + '%', height: 20 + 'px', backgroundColor: healthScale(this.props.snake.health), borderRadius: 5 + 'px'}}></div>
        </div>
        <div className="muted meta">
          {goldIndicator}
        </div>
        <div className={'taunt ' + tauntClass} style={tauntStyles}>{this.state.tauntToShow}</div>
      </div>
    )
  }
}
