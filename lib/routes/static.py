from flask import send_from_directory

from lib.server import app


@app.route('/static/<path:path>')
def server_static(path):
    # Flask has this built-in, but it's only active in dev
    return send_from_directory('static', path)
