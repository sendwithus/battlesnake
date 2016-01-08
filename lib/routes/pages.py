import markdown

from flask.ext.login import login_required

from lib.server import app


@app.route('/')
def index():
    return app.send_static_file('html/index.html')


@app.route('/code-of-conduct')
def code_of_conduct():
    f = open('static/md/code_of_conduct.md')
    html = markdown.markdown(f.read())
    f.close()
    return '<div style="width:600px">' + html + '</div>'


@app.route('/play/')
@app.route('/play/<path:path>')
@login_required
def play(path=None):
    # serve play.html for anything that starts with "play/"
    # frontend will show the correct route
    return app.send_static_file('html/play.html')
