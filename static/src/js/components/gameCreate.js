import React, { Component } from 'react';
import RouterContext from 'react-router';

export default class GameCreate extends Component {
  state = {
    availableTeams: [],
    addedTeams: [],
    selectedTeam: null,
    currentWidth: 20,
    currentHeight: 20,
    currentTimeout: 1,
    isLoading: false
  };

  _persistState () {
    localStorage['GameCreate.state'] = JSON.stringify(this.state);
  };

  _restoreState () {
    let oldState = {}
    let { state } = this.props.location

    try {
      oldState = JSON.parse(localStorage['GameCreate.state']);
    } catch (e) {
      // No state saved yet. Default it
    }

    // If were coming from a rematch
    if (state) {
      oldState.addedTeams = state.rematchTeams
    }

    this.setState($.extend(this.state, oldState));
  };

  handleGameCreate = (e) => {
    e.preventDefault();

    let gameData = {
      teams: this.state.addedTeams,
      width: parseInt(this.state.currentWidth),
      height: parseInt(this.state.currentHeight),
      turn_time: parseFloat(this.state.currentTimeout),
      mode: "advanced"
    };

    if (window.app.user.team.game_mode) {
      gameData.mode = window.app.user.team.game_mode
    }

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
          this.setState({isLoading: false});
          this.props.history.push('/app/games/' + response.data.game._id);
        }
        this._persistState();
      })
      .error((xhr, textStatus, errorThrown) => {
        alert(xhr.responseJSON.message);
        this.setState({isLoading: false});
      });
  };

  handleWidthChange = (e) => {
    this.setState({currentWidth: e.target.value});
  };

  handleHeightChange = (e) => {
    this.setState({currentHeight: e.target.value});
  };

  handleTeamChange = (e) => {
    let i = parseInt(e.target.value, 10);
    let team = this.state.availableTeams[i];
    this.setState({selectedTeam: team});
  };

  handleDeleteTeam = (i, e) => {
    let availableTeams = this.state.availableTeams;
    let addedTeams = this.state.addedTeams;

    let team = addedTeams[i];
    availableTeams.push(team);
    addedTeams.splice(i, 1);

    this.setState({
      addedTeams: addedTeams,
      availableTeams: availableTeams
    });
  };

  handleAddTeam = (e) => {
    e.preventDefault();
    let currentTeam = this.state.selectedTeam;
    let addedTeams = this.state.addedTeams;

    addedTeams.push(currentTeam);

    this.setState({
      selectedTeam: null,
      addedTeams: addedTeams
    });
  };

  componentDidMount () {
    this._restoreState();

    // fetch list of teams
    $.ajax({
      type: 'GET',
      url: '/api/teams/'
    })
    .done((response) => {
      this.setState({availableTeams: response.data});
    });
  }

  render () {
    let teamOpts = [];

    let availableTeamOptions = this.state.availableTeams.map((team, i) => {
      let teamname = team.teamname;
      if (['bounty', 'test'].includes(team.type)) {
        teamname = `${teamname} (${team.type} snake)`
      }

      let disabled = false;
      for (let j = 0; j < this.state.addedTeams.length; j++) {
        let t = this.state.addedTeams[j];
        let isAddedAlready = t._id === team._id;
        if (isAddedAlready) {
          disabled = true;
          teamname = `${teamname} - Added`;
          break;
        }
      }

      return (
        <option key={'team_opt_' + i} value={i} disabled={disabled}>
          {teamname}
        </option>
      );
    })

    teamOpts = teamOpts.concat(
      <option key="team_opt_none" value="none">Select a team</option>,
      availableTeamOptions
    );

    let teamNames = this.state.addedTeams.map((team, i) => {
      return (
        <li key={'team_' + i}>
          <a href="#"
             className="pull-right"
             onClick={this.handleDeleteTeam.bind(null, i)}>
            &times;
          </a>
          <p>{team.teamname}</p>
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
                          className="form-control"
                          onChange={this.handleTeamChange}>
                    {teamOpts}
                  </select>
                  <span className="input-group-btn">
                    <button type="submit"
                            className="btn btn-success"
                            disabled={this.state.selectedTeam ? false : 'disabled'}
                            onClick={this.handleAddTeam}>
                      Add Team
                    </button>
                  </span>
                </div>
              </div>
              <div className="form-group">
                <label>Width</label>
                <input type="number"
                       className="form-control"
                       placeholder="width"
                       min="5"
                       max="50"
                       value={this.state.currentWidth}
                       onChange={this.handleWidthChange}
                />
              </div>
              <div className="form-group">
                <label>Height</label>
                <input type="number"
                       className="form-control"
                       placeholder="height"
                       min="5"
                       max="50"
                       value={this.state.currentHeight}
                       onChange={this.handleHeightChange}
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
