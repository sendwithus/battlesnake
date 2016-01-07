import React from "react";

import Navbar from "./components/navbar";


export default class App extends React.Component {
  static propTypes = {
    children: React.PropTypes.node
  };

  displayName = "BattleSnake";

  render() {
    return (
      <div className="App">
        <Navbar />
        <div className="container-fluid">
          {this.props.children}
        </div>
      </div>
    );
  }
}
