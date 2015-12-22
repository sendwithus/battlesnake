import React from "react";
import ga from "react-google-analytics";
import env from "./config/environment";

import Navbar from "./components/Navbar";

const GAInitializer = ga.Initializer;

export default class App extends React.Component {
  constructor () {
    super()

    this.displayName = "App"

    this.propTypes = {
      children: React.PropTypes.node,
    }
  }

  componentDidMount() {
    ga("create", env.gaId, "auto");
    ga("send", "pageview");
  }

  render() {
    console.log(this.props)
    return (
      <div className="App">
        <Navbar />
        <div className="container-fluid">
          {this.props.children}
        </div>
        <GAInitializer />
      </div>
    );
  }
}
