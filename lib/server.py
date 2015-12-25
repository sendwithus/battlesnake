from flask import (
    Flask,
    jsonify, send_from_directory,
)
# Use hardcoded app name to ensure lib is not used for top-level directory
app = Flask('battlesnake')


def _json_response(data={}, msg=None, status=200):
    return jsonify(
        data=data,
        message=msg,
    ), status, {'Content-Type': 'application/json'}


def _json_error(msg=None, status=400):
    return jsonify(message=str(msg)), status, {'Content-Type': 'application/json'}


@app.route('/')
def index():
    return app.send_static_file('html/index.html')


@app.route('/play/')
@app.route('/play/<path:path>')
def page(path=None):
    # serve play.html for anything that starts with "play/"
    # frontend will show the correct route
    return app.send_static_file('html/play.html')


@app.route('/static/<path:path>')
def server_static(path):
    # Flask has this built-in, but it's only active in dev
    return send_from_directory('static', path)


@app.errorhandler(BaseException)
def server_error(e):
    # Generic handler for exceptions thrown when handling API requests
    # Others can be added for more specific exceptions with new errorhandler routes
    app.logger.exception(e)
    return _json_error(msg='Server error', status=500)


import lib.routes

# Expose WSGI app
application = app
