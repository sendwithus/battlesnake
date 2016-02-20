import React, { Component } from 'react';

export default class Navbar extends Component {

  static defaultProps = {
    links: [
      // Default nav links
      ['/app/games/tournament', 'Tournament'],
      ['/app/games', 'Games'],
      ['/app/game/new', 'New'],
      ['/team', 'My Team'],
      ['/logout', 'Logout']
    ]
  };

  state = {
    mobileNavExpanded: false
  };

  handleNavToggle = () => {
    this.setState({ mobileNavExpanded: !this.state.mobileNavExpanded });
  };

  handleNavChange = (link) => {
    this.setState({ mobileNavExpanded: false });
  };

  render () {
    let navToggleClass = this.state.mobileNavExpanded ? 'in': '';

    // Generate nav links
    let navLinks = this.props.links.map((link, i) => {
      return (
        <li key={i}>
          <a href={link[0]} onClick={this.handleNavChange.bind(null, link[0])}>
            {link[1]}
          </a>
        </li>
      );
    });

    return (
      <nav className="navbar navbar-inverse">
        <div className="container-fluid">
          <div className="navbar-header">
            <a className="navbar-brand" href="/app/games">
              <img src="/static/img/logo-slim.png" />
            </a>
            <button type="button"
                className="navbar-toggle collapsed"
                onClick={this.handleNavToggle}>
              <span className="sr-only">Toggle navigation</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
          </div>
          <div className={'collapse navbar-collapse site-links ' + navToggleClass}>
            <ul className="nav navbar-nav">{navLinks}</ul>
          </div>
        </div>
      </nav>
    );
  }
}
