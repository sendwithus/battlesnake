/** @jsx React.DOM */

var Sidebar = React.createClass({
    render: function () {
        return (
            <div className="sidebar-inner">
                <h3>{this.props.gameId}</h3>
                <ul>
                	<li>Snake 1</li>
                	<li>Snake 2</li>
                	<li>Snake 3</li>
                	<li>Snake 4</li>
                </ul>
            </div>
        );
    }
});

