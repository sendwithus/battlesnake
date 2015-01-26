/** @jsx React.DOM */

var Navbar = React.createClass({
    handleNavToggle: function () {
        this.setState({ mobileNavExpanded: !this.state.mobileNavExpanded });
    },
    handleNavChange: function (link) {
        this.setState({ mobileNavExpanded: false });
        this.props.onPageChange(link);
    },
    getInitialState: function () {
        return { mobileNavExpanded: false };
    },
    getDefaultProps: function () {
        return {
            links: [ // Default nav links
                ['#', 'Watch'],
                ['#games', 'Games'],
                ['#contact', 'Contact']
            ]
        };
    },
    render: function () {
        var navToggleClass = this.state.mobileNavExpanded ? 'in': '';

        // Generate nav links
        var navLinks = this.props.links.map(function (link, i) {
            return (
                <li key={i}>
                    <a href={link[0]} onClick={this.handleNavChange.bind(null, link[0])}>
                        {link[1]}
                    </a>
                </li>
           );
        }.bind(this));

        return (
            <nav className="navbar navbar-inverse">
                <div className="container-fluid">
                    <div className="navbar-header">
                        <a className="navbar-brand" href="#">Battle Snake</a>
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
});
