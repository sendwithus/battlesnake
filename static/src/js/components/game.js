/**
 * Any reference of _isMounted, see # see https://facebook.github.io/react/blog/2015/12/16/ismounted-antipattern.html
 */

import React, { Component } from 'react';
import navigate from 'react-router';

import Board from './board';
import GameSidebar from './gameSidebar'
import GameOverModal from './gameOverModal'


export default class Game extends Component {

  state = {
    game: null,
    isReplay: false,
    isLoading: false,
    latestGameState: null,
    turnNumber: 0
  };

  handlePause = () => {
    $.ajax({
        type: 'PUT',
        url: '/api/games/' + this.props.params.id + '/pause'
      })
      .done((response) => {
        console.log('Paused Game', response.data);
        this.setState({game: response.data});
      });
  };

  handleResume = () => {
    $.ajax({
        type: 'PUT',
        url: '/api/games/' + this.props.params.id + '/resume'
      })
      .done((response) => {
        console.log('Resumed Game', response.data);
        this.setState({game: response.data});
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
            setTimeout(next, 300);
          }
        };

        next();
      });

    this.setState({isReplay: true});
  };

  handleCancelReplay = () => {
    this.setState({isReplay: false});
  };

  handleClickNextTurn = () => {
    this.setState({isLoading: true});
    $.ajax({
        type: 'POST',
        url: '/api/games/' + this.props.params.id + '/turn'
      })
      .done((response) => {
        this.handleGameState(response.data);
      });
  };

  handleRematch = () => {
    this.setState({isLoading: true, turnNumber: 0});

    $.ajax({
        type: 'POST',
        url: '/api/games/' + this.props.params.id + '/rematch'
      })
      .done((response) => {
        this.props.history.push('/app/games/' + response.data._id);
        this.componentDidMount();
      })
      .error((xhr, textStatus, errorThrown) => {
        this.setState({isLoading: false});
      });
  };

  handleStart (isManual) {
    let formData = JSON.stringify({manual: isManual});
    $.ajax({
        type: 'POST',
        url: '/api/games/' + this.props.params.id + '/start',
        data: formData
      })
      .done((response) => {
        console.log('Started Game', response.data);
        this.setState({game: response.data});
        this.checkInterval();
      });
  }

  handleGameState (gameState, ignoreEnd) {
    if (this._isMounted) {
      //console.log('GAME STATE', gameState);
      this.state.latestGameState = gameState;
      this.state.isLoading = false;
      this.state.turnNumber = gameState.turn + 1;

      if (gameState.is_done) {
        $('#game-summary-modal').off('shown.bs.modal').on('shown.bs.modal', () => {
          $(this).find('button').focus();
        }).modal('show');

        this.state.isReplay = false;
        this.state.game.state = 'done';
      }

      this.setState(this.state);
    }
  }

  tick (callback) {
    let url = '';
    if (this.state.turnNumber > 0) {
      url = `/api/games/${this.props.params.id}/gamestates/turn/${this.state.turnNumber}`;
    } else {
      // If we're on the first turn, get the latest. This is so we always start at the latest state
      url = `/api/games/${this.props.params.id}/gamestates/latest`;
    }

    $.ajax({type: 'GET', url: url})
      .done((response) => {
        this.handleGameState(response.data);
        callback && callback(null, response.data);
      })
      .error(() => {
        callback && callback(new Error('Failed to fetch gamestate'));
      });
  }

  checkInterval () {
    let shouldTick = this.state.game.state === 'playing' || this.state.game.state === 'ready';
    if (!shouldTick) {
      return;
    }

    let startTimestamp = Date.now();
    this.tick((gameState, err) => {
      let endTimestamp = Date.now();
      let elapsedMillis = endTimestamp - startTimestamp;

      let sleepFor = Math.max(this.state.game.turn_time, this.state.game.turn_time * 1000 - elapsedMillis);

      if (err) {
        // If there was an error fetching state, just retry it later...
        requestTimeout(this.checkInterval.bind(this), sleepFor);
        return;
      }

      if (this._isMounted && shouldTick && !gameState.is_done) {
        requestTimeout(this.checkInterval.bind(this), sleepFor);
      }

      if (gameState.is_done) {
        this.state.game.state = 'done';
        this.setState({game: this.state.game});
      }
    });
  }

  componentDidMount () {
    this._isMounted = true;
    $.ajax({
        type: 'GET',
        url: '/api/games/' + this.props.params.id
      })
      .done((response) => {
        if (this._isMounted) {
          this.setState({game: response.data});
        }

        // Get latest game state
        this.tick(() => {
          // See if we need to tick the game
          this.checkInterval();
        });
      });
  }

  componentDidUpdate (prevProps, prevState) {
    if (!this.state.latestGameState) {
      return;
    }
    if (!this.board) {
      this.board = this.getBoard();
      this.board.init(this.state.latestGameState);
    }

    this.board.update(this.state.latestGameState);
  }

  componentWillUnmount () {
    this._isMounted = false;
  }

  getBoard () {
    return new Board(this.refs.board);
  }

  render () {
    return (
      <div className={"row game-wrapper hash-" + window.location.hash.replace('#', '')}>
        <div className="col-md-9 left">
          <div ref="board"></div>
        </div>
        <div className="col-md-3 sidebar right">
          <GameSidebar
            id={this.props.params.id}
            game={this.state.game}
            isReplay={this.state.isReplay}
            isLoading={this.state.isLoading}
            latestGameState={this.state.latestGameState}
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
