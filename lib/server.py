from flask import (
    Flask,
    request,
    jsonify,
    flash,
    redirect,
    url_for,
)

from lib.log import get_logger

logger = get_logger(__name__)

# Use hardcoded app name to ensure lib is not used for top-level directory
app = Flask('battlesnake')


def json_response(data={}, msg=None, status=200):
    return jsonify(
        data=data,
        message=msg,
    ), status, {'Content-Type': 'application/json'}


def json_error(msg=None, status=400):
    logger.exception('ROUTE ERROR:')
    return jsonify(message=str(msg)), status, {'Content-Type': 'application/json'}


def form_error(msg, view=None):
    if view is None:
        view = request.endpoint

    flash(msg, 'error')
    return redirect(url_for(view))

import lib.routes

# Expose WSGI app
application = app
