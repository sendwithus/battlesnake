from flask.ext.login import login_required

from lib.server import app


@app.route('/')
def index():
    return app.send_static_file('src/html/index.html')


@app.route('/play/')
@app.route('/play/<path:path>')
@login_required
def play(path=None):
    # serve play.html for anything that starts with "play/"
    # frontend will show the correct route
    return app.send_static_file('src/html/play.html')
