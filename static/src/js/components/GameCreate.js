import {Component} from 'react';
import {navigate} from 'react-router';


class GameCreate extends Component {

  _loadPastState () {
    try {
      return JSON.parse(window.localStorage['battlesnake.new_game_state']);
    } catch (e) {
      return null;
    }
  }

  _savePastState () {
    let json = JSON.stringify(this.state);
    window.localStorage['battlesnake.new_game_state'] = json;
  }

  handleGameCreate (e) {
    e.preventDefault();

    let gameData = {
      snake_urls: this.state.snakeUrls,
      width: parseInt(this.state.currentWidth),
      height: parseInt(this.state.currentHeight),
      turn_time: parseFloat(this.state.currentTimeout),
    };

    this.setState({ isLoading: true });

    $.ajax({
      type: 'POST',
      url: '/api/games',
      data: JSON.stringify(gameData),
      contentType: 'application/json'
    })
    .done((response) => {
      if (response.data.error) {
        alert(response.data.message);
      } else {
        this._savePastState();
        navigate('/play/games/' + response.data.game._id);
      }
      this.setState({ isLoading: false });
    })
    .error((xhr, textStatus, errorThrown) => {
      alert(xhr.responseJSON.message);
      this.setState({ isLoading: false });
    });
  }

  handleSubmitSnake (e) {
    e.preventDefault();
    let snakeUrl  = this.state.currentSnakeUrl;
    let snakeUrls = this.state.snakeUrls;
    if (!snakeUrl.match(/^[a-zA-Z]+:\/\//)) {
      snakeUrl = 'http://' + snakeUrl;
    }
    if(snakeUrl.substr(-1) === '/') {
      snakeUrl = snakeUrl.substr(0, snakeUrl.length - 1);
    }
    snakeUrls.push(snakeUrl.toLowerCase());
    this.setState({ snakeUrls: snakeUrls, currentSnakeUrl: '' });
  }

  handleSnakeUrlChange (e) {
    this.setState({ currentSnakeUrl: e.target.value });
  }

  handleDeleteSnakeUrl (i, e) {
    let snakeUrls = this.state.snakeUrls;
    snakeUrls.splice(i, 1);
    this.setState({ snakeUrls: snakeUrls });
  }

  handleWidthChange (e) {
    this.setState({ currentWidth: e.target.value });
  }

  handleHeightChange (e) {
    this.setState({ currentHeight: e.target.value });
  }

  handleTimeoutChange (e) {
    this.setState({ currentTimeout: e.target.value });
  }

  getInitialState () {
    let state = this._loadPastState();
    if (state) {
      state.isLoading = false;
      return state;
    }

    return {
      snakeUrls: [ ],
      currentSnakeUrl: '',
      currentWidth: 20,
      currentHeight: 20,
      currentTimeout: 1,
      isLoading: false
    };
  }

  render () {
    let noSnakesMessage = '';
    let snakeUrls = this.state.snakeUrls.map((snakeUrl, i) => {
      return (
        <div key={'url_' + i}>
          <a href="#"
            className="pull-right"
            onClick={this.handleDeleteSnakeUrl.bind(null, i)}>
            &times;
          </a>
          <p>{snakeUrl}</p>
        </div>
      );
    });

    if (!this.state.snakeUrls.length) {
      noSnakesMessage = (
        <p>You have no snake added. Input your snake url in the box below...</p>
      );
    }

    return (
      <div className="container">
        <form onSubmit={this.handleSubmitSnake}>
          <h2>Create Game</h2>
          <br />
          {noSnakesMessage}
          <div>
            {snakeUrls}
          </div>
          <div className="input-group">
            <input type="text"
              className="form-control"
              value={this.state.currentSnakeUrl}
              name="snake-url"
              placeholder="http://mysnake.herokuapp.com"
              onChange={this.handleSnakeUrlChange}
            />
            <span className="input-group-btn">
              <button type="submit"
                disabled={this.state.currentSnakeUrl ? false : 'on'}
                className="btn btn-info big form-control">
                Add Snake
              </button>
            </span>
          </div>
          <div className="row">
              <div className="col-md-4">
                  <label>width</label>
                  <input type="number"
                      className="form-control"
                      placeholder="width"
                      min="5"
                      max="50"
                      value={this.state.currentWidth}
                      onChange={this.handleWidthChange}/>
              </div>
              <div className="col-md-4">
                <label>height</label>
                <input type="number"
                  className="form-control"
                  placeholder="height"
                  min="5"
                  max="50"
                  value={this.state.currentHeight}
                  onChange={this.handleHeightChange}
                />
              </div>
              <div className="col-md-4">
                <label>turn time</label>
                <input type="number"
                  step="0.1"
                  min="0.1"
                  className="form-control"
                  placeholder="1.0 (seconds)"
                  value={this.state.currentTimeout}
                  onChange={this.handleTimeoutChange}
                />
              </div>
          </div>
          <div className="input-group">
            <button type="button" className="btn btn-big btn-success" onClick={this.handleGameCreate} disabled={this.state.isLoading}>
              {this.state.isLoading ? 'Contacting snakes...' : 'Start Game'}
            </button>
          </div>
        </form>
      </div>
    );
  }

}
