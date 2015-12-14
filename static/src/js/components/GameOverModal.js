class GameOverModal extends React.Component {

  render () {
    if (!this.props.game || !this.props.latestGameState) {
      return <div></div>;
    }

    let winningSnake;

    if (this.props.latestGameState.snakes.length === 1) {
      winningSnake = this.props.latestGameState.snakes[0].name;
    } else {
      winningSnake = 'N/A';
    }

    return (
      <div className="modal fade" id="game-summary-modal" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <h4 className="modal-title">
                Finished {this.props.game.id}
              </h4>
            </div>
            <div className="modal-body">
              Winner: {winningSnake}
            </div>
            <div className="modal-footer">
              <button type="submit" className="btn btn-success" data-dismiss="modal">Continue</button>
            </div>
          </div>
        </div>
      </div>
    );
  }

}
