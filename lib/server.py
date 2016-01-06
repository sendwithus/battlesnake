from flask import (
    Flask,
    request,
    jsonify, flash, redirect,
    url_for,
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


def _form_error(msg, view=None):
    if view is None:
        view = request.endpoint

    flash(msg, 'error')
    return redirect(url_for(view))

import lib.routes

# Expose WSGI app
application = app
