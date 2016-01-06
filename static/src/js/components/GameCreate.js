import React, { Component } from 'react';
import RouterContext from 'react-router';


export default class GameCreate extends Component {

  constructor () {
    super()

    let state = this._loadPastState();
    if (state) {
      state.isLoading = false;
      if(!state.teamnames || !state.availableTeams) {
        state.availableTeams = [];
        state.teamnames = [];
      }
    }

    this.state = state || {
      availableTeams: [],
      teamnames: [],
      snakeUrls: [],
      currentSnakeUrl: '',
      selectedTeamName: '',
      currentWidth: 20,
      currentHeight: 20,
      currentTimeout: 1,
      isLoading: false
    };
  }

  componentDidMount () {
    // fetch list of teams
    $.ajax({
      type: 'GET',
      url: '/api/teams/',
    })
    .done((response) => {
      this.setState({ availableTeams: response.data });
    });
  }

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

  handleGameCreate = (e) => {
    e.preventDefault();

    let gameData = {
      snake_urls: this.state.snakeUrls,
      teamnames: this.state.teamnames,
      width: parseInt(this.state.currentWidth),
      height: parseInt(this.state.currentHeight),
      turn_time: parseFloat(this.state.currentTimeout),
    };

    this.setState({ isLoading: true });

    $.ajax({
      type: 'POST',
      url: '/api/games',
      data: JSON.stringify(gameData)
    })
    .done((response) => {
      if (response.data.error) {
        alert(response.data.message);
        this.setState({ isLoading: false });
      } else {
        this._savePastState();
        this.setState({ isLoading: false });
        this.props.history.push('/play/games/' + response.data.game._id);
      }
    })
    .error((xhr, textStatus, errorThrown) => {
      alert(xhr.responseJSON.message);
      this.setState({ isLoading: false });
    })
  }

  handleSubmitSnake = (e) => {
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

  handleSnakeUrlChange = (e) => {
    this.setState({ currentSnakeUrl: e.target.value });
  }

  handleDeleteSnakeUrl = (i, e) => {
    let snakeUrls = this.state.snakeUrls;
    snakeUrls.splice(i, 1);
    this.setState({ snakeUrls: snakeUrls });
  }

  handleWidthChange = (e) => {
    this.setState({ currentWidth: e.target.value });
  }

  handleHeightChange = (e) => {
    this.setState({ currentHeight: e.target.value });
  }

  handleTimeoutChange = (e) => {
    this.setState({ currentTimeout: e.target.value });
  }

  handleTeamChange = (e) => {
    this.setState({ selectedTeamName: e.target.value });
  }

  handleDeleteTeam = (i, e) => {
    let teamnames = this.state.teamnames;
    teamnames.splice(i, 1);
    this.setState({ teamnames: teamnames });
  }

  handleSubmitTeam = (e) => {
    e.preventDefault();
    let teamnames = this.state.teamnames;
    teamnames.push(this.state.selectedTeamName);
    this.setState({ teamnames: teamnames, selectedTeamName: '' });
  }

  render () {
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

    let noSnakesMessage = '';
    if (!this.state.snakeUrls.length) {
      noSnakesMessage = (
        <p>You have no snake added. Input your snake url in the box below...</p>
      );
    }

    let noTeamsMessage = '';
    if (!this.state.teamnames.length) {
      noTeamsMessage = (
        <p>You have no teams added. Select a team in the box below...</p>
      );
    }

    let teamsByName = {};
    let teamOpts = this.state.availableTeams.map((team, i) => {
      teamsByName[team.teamname] = team;
      return (
        <option key={'team_opt_' + i} value={team.teamname}>
          {team.teamname}
        </option>
      );
    });

    let teamnames = this.state.teamnames.map((teamname, i) => {
      let team = teamsByName[teamname];
      return (
        <div key={'team_' + i}>
          <a href="#"
             className="pull-right"
             onClick={this.handleDeleteTeam.bind(null, i)}>
            &times;
          </a>
          <p><strong>{teamname}</strong> - {team.snake_url}</p>
        </div>
      );
    });

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

            {noTeamsMessage}
            <div>
              {teamnames}
            </div>
            <div className="input-group">
              <select name="teamname"
                      className="form-control"
                      onChange={this.handleTeamChange}>
                <option value="">Select a team</option>
                {teamOpts}
              </select>
              <span className="input-group-btn">
                <button type="submit"
                        disabled={this.state.selectedTeamName ? false : 'on'}
                        className="btn btn-info big form-control"
                        onClick={this.handleSubmitTeam}>
                    Add Team
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
                       onChange={this.handleWidthChange}
                  />
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
