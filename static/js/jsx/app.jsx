/** @jsx React.DOM */

var App = React.createClass({
    render: function () {
        return (
            <div>
                <Navbar />
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-md-9">
                            <Game />
                        </div>
                        <div className="col-md-3 sidebar">
                            <Sidebar />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

// Trigger the first render
window.onload = function () {
    React.render(<App />, document.getElementById('app'));
};
