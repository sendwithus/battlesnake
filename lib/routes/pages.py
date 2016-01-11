import markdown

from flask import Markup, render_template
from flask.ext.login import login_required

from lib.server import app


def __load_markdown(filepath):
    with open(filepath) as f:
        return Markup(markdown.markdown(f.read()))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/readme')
def readme():
    section_markdown = (
        '0-intro',
        '1-location',
        '2-preparing',
        '3-prizes',
        '4-bounty',
        '5-rules',
        '6-advanced',
        '7-starting',
        '8-api',
        '9-testing',
    )
    sections = [
        (section, __load_markdown('static/md/%s.md' % section))
        for section in section_markdown
    ]
    return render_template('readme.html', sections=sections)


@app.route('/code-of-conduct')
def code_of_conduct():
    return render_template('code_of_conduct.html')


@app.route('/play/')
@app.route('/play/<path:path>')
@login_required
def play(path=None):
    # serve play.html for anything that starts with "play/"
    # frontend will show the correct route
    return render_template('play.html')
