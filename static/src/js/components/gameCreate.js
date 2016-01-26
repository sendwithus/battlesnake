import React, { Component } from 'react';
import RouterContext from 'react-router';


export default class GameCreate extends Component {

  constructor () {
    super();

    let state = this._loadPastState();
    if (state) {
      state.isLoading = false;
      state.addedTeams = state.addedTeams || [];
      state.availableTeams = state.availableTeams || [];
      this.state = state;
    } else {
      this.state = {
        availableTeams: [],
        addedTeams: [],
        currentSnakeUrl: '',
        selectedTeam: null,
        currentWidth: 20,
        currentHeight: 20,
        currentTimeout: 1,
        isLoading: false
      };
    }
  }

  handleGameCreate = (e) => {
    e.preventDefault();

    let gameData = {
      teams: this.state.addedTeams,
      width: parseInt(this.state.currentWidth),
      height: parseInt(this.state.currentHeight),
      turn_time: parseFloat(this.state.currentTimeout)
    };

    this.setState({isLoading: true});

    $.ajax({
        type: 'POST',
        url: '/api/games',
        data: JSON.stringify(gameData)
      })
      .done((response) => {
        if (response.data.error) {
          alert(response.data.message);
          this.setState({isLoading: false});
        } else {
          this._savePastState();
          this.setState({isLoading: false});
          this.props.history.push('/app/games/' + response.data.game._id);
        }
      })
      .error((xhr, textStatus, errorThrown) => {
        alert(xhr.responseJSON.message);
        this.setState({isLoading: false});
      })
  };

  handleSubmitSnake = (e) => {
    e.preventDefault();
    let snakeUrl = this.state.currentSnakeUrl;
    let snakeUrls = this.state.snakeUrls;
    snakeUrls.push(snakeUrl.toLowerCase());
    this.setState({snakeUrls: snakeUrls, currentSnakeUrl: ''});
  };

  handleWidthChange = (e) => {
    this.setState({currentWidth: e.target.value});
  };

  handleHeightChange = (e) => {
    this.setState({currentHeight: e.target.value});
  };

  handleTimeoutChange = (e) => {
    this.setState({currentTimeout: e.target.value});
  };

  handleTeamChange = (e) => {
    let i = parseInt(e.target.value, 10);
    let team = this.state.availableTeams[i];
    window.EEE = e;
    this.setState({selectedTeam: team});
  };

  handleDeleteTeam = (i, e) => {
    let teams = this.state.addedTeams;
    teams.splice(i, 1);
    this.setState({addedTeams: teams});
  };

  handleAddTeam = (e) => {
    e.preventDefault();
    let team = this.state.selectedTeam;
    let teams = this.state.addedTeams;
    teams.push(team);
    this.setState({addedTeams: teams});
  };

  componentDidMount () {
    // fetch list of teams
    $.ajax({
        type: 'GET',
        url: '/api/teams/'
      })
      .done((response) => {
        this.setState({availableTeams: response.data});
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

  render () {
    let noTeamsMessage = '';
    if (!this.state.addedTeams.length) {
      noTeamsMessage = (
        <p>You have no teams added. Select a team in the box below...</p>
      );
    }

    let teamOpts = this.state.availableTeams.map((team, i) => {
      return (
        <option key={'team_opt_' + i} value={i}>
          {team.teamname}
        </option>
      );
    });

    let teamNames = this.state.addedTeams.map((team, i) => {
      return (
        <div key={'team_' + i}>
          <a href="#"
             className="pull-right"
             onClick={this.handleDeleteTeam.bind(null, i)}>
            &times;
          </a>
          <p><strong>{team.teamname}</strong> - {team.snake_url}</p>
        </div>
      );
    });

    return (
      <div className="container">
        <form onSubmit={this.handleSubmitSnake}>
          <h2>Create Game</h2>
          <br />
          {noTeamsMessage}
          <div>
            {teamNames}
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
                        disabled={this.state.selectedTeam ? false : 'on'}
                        className="btn btn-info big form-control"
                        onClick={this.handleAddTeam}>
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
            <button type="button" className="btn btn-lg btn-success"
                    onClick={this.handleGameCreate}
                    disabled={this.state.isLoading}>
              {this.state.isLoading ? 'Contacting snakes...' : 'Start Game'}
            </button>
          </div>
        </form>
      </div>
    );
  }

}
