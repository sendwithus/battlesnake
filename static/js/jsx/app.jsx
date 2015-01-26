/** @jsx React.DOM */

var App = React.createClass({
    handleHashChange: function (hash) {
        this.setState({ hash: hash });
    },
    componentDidMount: function () {
        this.handleHashChange(window.location.hash);
    },
    getInitialState: function () {
        return { };
    },
    render: function () {
        var page;

        if (this.state.hash === '#games') {
            page = (
                <div className="row">
                    <div className="col-md-12">
                        <h1>Games</h1>
                    </div>
                </div>
            );
        } else if (this.state.hash === '#contact') {
            page = (
                <div className="row">
                    <div className="col-md-12">
                        <h1>Contact</h1>
                    </div>
                </div>
            );
        } else {
            page = (
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

        return (
            <div>
                <Navbar onPageChange={this.handleHashChange} />
                <div className="container-fluid">
                    {page}
                </div>
            </div>
        );
    }
});

// Trigger the first render
window.onload = function () {
    React.render(<App />, document.getElementById('app'));
};
