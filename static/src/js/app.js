import React from "react";
import ga from "react-google-analytics";
import env from "./config/environment";

import Navbar from "./components/navbar";

// const GAInitializer = ga.Initializer;

export default class App extends React.Component {
  static propTypes = {
    children: React.PropTypes.node
  }

  // displayName = "BattleSnake"

  // componentDidMount() {
  //   ga("create", env.gaId, "auto");
  //   ga("send", "pageview");
  // }

  // <GAInitializer />
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
