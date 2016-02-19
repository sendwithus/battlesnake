import markdown

from flask import Markup, render_template


from lib.server import app
from lib.routes.auth import public


def __load_markdown(filepath):
    with open(filepath) as f:
        html = markdown.markdown(
            f.read(),
            extensions=['markdown.extensions.fenced_code']
        )
    return Markup(html)


@app.route('/')
@public
def index():
    return render_template('index.html')


@app.route('/setup')
@public
def setup():
    html = __load_markdown('static/md/setup.md')
    return render_template('markdown.html', html=html, title='Getting Started')


@app.route('/easy')
@public
def easy():
    html = __load_markdown('static/md/easy.md')
    return render_template('markdown.html', html=html, title='Getting Started')


@app.route('/readme')
@public
def readme():
    section_markdown = (
        '0-intro',
        '1-location',
        '2-preparing',
        '3-tournament',
        '4-bounty',
        '5-prizes',
        '6-rules-tease',
        '7-advanced-tease',
        '8-starting-tease',
        '9-api-tease',
        '10-testing-tease',
        '11-outro'
    )
    sections = [
        (section, __load_markdown('static/md/readme/%s.md' % section))
        for section in section_markdown
    ]
    return render_template('readme.html', sections=sections)


@app.route('/readme/secret')
@public
def secret_readme():
    section_markdown = (
        '0-intro',
        '1-location',
        '2-preparing',
        '3-tournament',
        '4-bounty',
        '5-prizes',
        '6-rules',
        '7-advanced',
        '8-starting',
        '9-api',
        '10-testing',
        '11-outro'
    )
    sections = [
        (section, __load_markdown('static/md/readme/%s.md' % section))
        for section in section_markdown
    ]
    return render_template('readme.html', sections=sections)


@app.route('/code-of-conduct')
@public
def code_of_conduct():
    return render_template('code_of_conduct.html')


@app.route('/app/')
@app.route('/app/<path:path>')
def app_paths(path=None):
    # serve app.html for anything that starts with "app/"
    # frontend will show the correct route
    return render_template('app.html')
