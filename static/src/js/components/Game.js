/**
 * Any reference of _isMounted, see # see https://facebook.github.io/react/blog/2015/12/16/ismounted-antipattern.html
 */

import React, { Component } from 'react';
import navigate from 'react-router';

import Board from './board';
import GameSidebar from './gameSidebar'
import GameOverModal from './gameOverModal'


export default class Game extends Component {

  state =  {
    game: null,
    isReplay: false,
    isLoading: false,
    latestGameState: null
  };

  handlePause = () => {
    $.ajax({
      type: 'PUT',
      url: '/api/games/' + this.props.params.id + '/pause'
    })
    .done((response) => {
      console.log('Paused Game', response.data);
      this.setState({ game: response.data });
    });
  };

  handleResume = () => {
    $.ajax({
      type: 'PUT',
      url: '/api/games/' + this.props.params.id + '/resume'
    })
    .done((response) => {
      console.log('Resumed Game', response.data);
      this.setState({ game: response.data });
      this.checkInterval();
    });
  };

  handleReplay = () => {
    console.log('Started Replay');
    let url = '/api/games/' + this.props.params.id + '/gamestates';

    $.ajax({
      type: 'GET',
      url: url
    })
    .done((response) => {
      let framesCompleted = 0;
      let gameStates = response.data;

      let next = () => {
        this.handleGameState(gameStates[gameStates.length - framesCompleted - 1]);
        if (++framesCompleted < response.data.length && this.state.isReplay) {
          setTimeout(next, 350);
        }
      };

      next();
    });

    this.setState({ isReplay: true });
  };

  handleCancelReplay = () => {
    this.setState({ isReplay: false });
  };

  handleClickNextTurn = () => {
    this.setState({ isLoading: true });
    $.ajax({
      type: 'POST',
      url: '/api/games/' + this.props.params.id + '/turn'
    })
    .done((response) => {
      this.handleGameState(response.data);
    });
  };

  handleRematch = () => {
    this.setState({ isLoading: true });

    $.ajax({
      type: 'POST',
      url: '/api/games/' + this.props.params.id + '/rematch'
    })
    .done((response) => {
      this.props.history.push('/play/games/' + response.data._id);
      this.componentDidMount();
    })
    .error((xhr, textStatus, errorThrown) => {
      this.setState({ isLoading: false });
    });
  };

  handleClickContinuous = () => {
    this.interval = setInterval(this.handleClickNextTurn, 400);
  };

  handleStart (isManual) {
    let formData = JSON.stringify({ manual: isManual })
    console.log(formData);
    $.ajax({
      type: 'POST',
      url: '/api/games/' + this.props.params.id + '/start',
      data: formData,
    })
    .done((response) => {
      console.log('Started Game', response.data);
      this.setState({ game: response.data });
      this.checkInterval();
    });
  }

  handleGameState (gameState, ignoreEnd) {
    if (this._isMounted) {
      console.log('GAME STATE', gameState);
      this.state.latestGameState = gameState;
      this.state.isLoading = false;

      if (gameState.is_done) {
        $('#game-summary-modal').off('shown.bs.modal').on('shown.bs.modal', () => {
          console.log('hello');
          $(this).find('button').focus();
        }).modal('show');

        this.state.isReplay = false;
        this.state.game.state = 'done';
      }

      this.setState(this.state);
    }
  }

  tick (callback) {
    let url = '/api/games/' + this.props.params.id + '/gamestates/latest';
    let id = Date.now();

    $.ajax({ type: 'GET', url: url })
    .done((response) => {
      this.handleGameState(response.data);
      callback && callback(response.data);
    });
  }

  checkInterval () {
    let _ = () => {
      let shouldTick = this.state.game.state === 'playing' ||
                       this.state.game.state === 'ready';
      if (!shouldTick) { return; }

      let startTimestamp = Date.now();
      this.tick((gameState) => {
        let endTimestamp = Date.now();
        let elapsedMillis = endTimestamp - startTimestamp;

        let sleepFor = Math.max(0, this.state.game.turn_time * 1000 - elapsedMillis);

        if (this._isMounted && shouldTick && !gameState.is_done) {
          setTimeout(_, sleepFor);
        }

        if (gameState.is_done) {
          this.state.game.state = 'done';
          this.setState({ game: this.state.game });
        }
      });
    };

    _();
  }

  componentDidMount () {
    this._isMounted = true;
    let canvas = this.refs.canvas;
    $.ajax({
      type: 'GET',
      url: '/api/games/' + this.props.params.id
    })
    .done((response) => {
      console.log(response);
      if (this._isMounted) {
        this.setState({ game: response.data });
      }

      // Get latest game state
      this.tick(() => {
        // See if we need to tick the game
        this.checkInterval();
      });
    });
  }

  componentDidUpdate (prevProps, prevState) {
    if (!this.state.latestGameState) { return; }

    if (!this.board) {
      this.board = this.getBoard();
      this.board.init(this.state.game.width, this.state.game.height);
    }

    this.board.update(this.state.latestGameState );
  }

  componentWillUnmount () {
    this._isMounted = false;
  }

  getBoard () {
    return new Board(this.refs.board);
  }

  render () {
    return (
      <div className="row">
        <div className="col-md-9">
          <div ref="board"></div>
        </div>
        <div className="col-md-3 sidebar">
          <GameSidebar
            id={this.props.params.id}
            game={this.state.game}
            isReplay={this.state.isReplay}
            isLoading={this.state.isLoading}
            latestGameState={this.state.latestGameState}
            continuous={this.handleClickContinuous}
            startAutomated={this.handleStart.bind(this, false)}
            startManual={this.handleStart.bind(this, true)}
            startReplay={this.handleReplay}
            rematch={this.handleRematch}
            cancelReplay={this.handleCancelReplay}
            pause={this.handlePause}
            resume={this.handleResume}
            nextTurn={this.handleClickNextTurn}
          />
        </div>
        <GameOverModal
          game={this.state.game}
          latestGameState={this.state.latestGameState}
        />
      </div>
    );
  }

}
