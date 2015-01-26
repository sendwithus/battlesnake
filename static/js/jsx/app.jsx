/** @jsx React.DOM */

var Wrapper = React.createClass({
    render: function () {
        return (
            <div className="row">
                <div className="col-md-9">
                    <Game />
                </div>
                <div className="col-md-3 sidebar">
                    <Sidebar />
                </div>
            </div>
        );
    }
});

// Trigger the first render
React.render(<Wrapper />, document.getElementById('wrapper'));
