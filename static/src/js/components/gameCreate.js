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
    // window.EEE = e;
    this.setState({selectedTeam: team});
  };

  handleDeleteTeam = (i, e) => {
    let teams = this.state.addedTeams;
    teams.splice(i, 1);
    this.setState({addedTeams: teams});
  };

  handleAddTeam = (e) => {
    e.preventDefault();
    let currentTeam = this.state.selectedTeam;
    let allTeams = this.state.addedTeams;
    let availableTeams = this.state.availableTeams;

    allTeams.push(currentTeam);

    _.remove(availableTeams, (team) => {
      return team._id === currentTeam._id
    });

    let state = {
      selectedTeam: null,
      addedTeams: allTeams,
      availableTeams: availableTeams
    }

    this.setState(state);
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
    let teamOpts = this.state.availableTeams.map((team, i) => {
      return (
        <option key={'team_opt_' + i} value={i}>
          {team.teamname}
        </option>
      );
    });

    let teamNames = this.state.addedTeams.map((team, i) => {
      return (
        <li key={'team_' + i}>
          <a href="#"
             className="pull-right"
             onClick={this.handleDeleteTeam.bind(null, i)}>
            &times;
          </a>
          <p><strong>{team.teamname}</strong></p>
        </li>
      );
    });

    if (this.state.addedTeams.length === 0) {
      teamNames.push(
        <li key="team_no_team_selected">
          <p>You have no teams added. Select a team in the box below...</p>
        </li>
      );
    }

    return (
      <div className="container">
        <form>
          <div className="row">
            <div className="col-md-12">
              <h2>Create Game</h2>
              <br />
            </div>
          </div>
          <div className="row">
            <div className="col-md-5">
              <h3>Teams Entering The Game:</h3>
              <ul className="team-member-list list-unstyled">
                {teamNames}
              </ul>
            </div>
            <div className="col-md-5 col-md-push-2">
              <div className="form-group">
                <label>Add a team</label>
                <div className="input-group ">
                  <select name="teamname"
                          className="form-control "
                          onChange={this.handleTeamChange}>
                    <option value="">Select a team</option>
                    {teamOpts}
                  </select>
                  <span className="input-group-btn">
                    <button type="submit"
                            className="btn btn-success"
                            disabled={this.state.selectedTeam || this.state.availableTeams.length !== 0 ? false : 'disabled'}
                            onClick={this.handleAddTeam}>
                      Add Team
                    </button>
                  </span>
                </div>
              </div>
              <div className="form-group">
                <label>width</label>
                <input type="number"
                       className="form-control "
                       placeholder="width"
                       min="5"
                       max="50"
                       value={this.state.currentWidth}
                       onChange={this.handleWidthChange}
                />
              </div>
              <div className="form-group">
                <label>height</label>
                <input type="number"
                       className="form-control "
                       placeholder="height"
                       min="5"
                       max="50"
                       value={this.state.currentHeight}
                       onChange={this.handleHeightChange}
                />
              </div>
              <div className="form-group">
                <label>turn time</label>
                <input type="number"
                       step="0.1"
                       min="0.1"
                       className="form-control "
                       placeholder="1.0 (seconds)"
                       value={this.state.currentTimeout}
                       onChange={this.handleTimeoutChange}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <br />
              <button type="button"
                      className="btn btn-lg btn-block btn-success"
                      onClick={this.handleGameCreate}
                      disabled={this.state.isLoading}>
                {this.state.isLoading ? 'Contacting snakes...' : 'Start Game'}
              </button>
            </div>
          </div>
        </form>
      </div>
    );
  }

}
