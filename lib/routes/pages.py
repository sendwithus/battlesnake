import markdown
import requests

from flask import Markup, redirect, render_template, url_for


from lib.server import app
from lib.routes.auth import public


def __load_markdown(filepath):
    if '4-bounty' in filepath:
        BOUNTY_MD_URL = 'https://www.dropbox.com/s/zfn90l5uxvf5poj/bounty.md?dl=1'
        r = requests.get(BOUNTY_MD_URL)
        html = markdown.markdown(
            r.text,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite'
            ]
        )

        return Markup(html)

    with open(filepath) as f:
        html = markdown.markdown(
            f.read(),
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite'
            ]
        )
    return Markup(html)


@app.route('/')
@public
def index():
    return render_template('index.html')


@app.route('/feedback')
@public
def feedback():
    return redirect(
        'https://sendwithus.wufoo.com/forms/zruoyzf026vi9i/',
        code=301
    )


@app.route('/tutorial')
@public
def setup():
    html = __load_markdown('static/md/tutorial.md')
    return render_template('markdown.html', html=html, title='Getting Started')


@app.route('/github')
@public
def tutorial_github():
    html = __load_markdown('static/md/github.md')
    return render_template('markdown.html', html=html, title='Getting Started')


@app.route('/local')
@public
def easy():
    html = __load_markdown('static/md/local.md')
    return render_template('markdown.html', html=html, title='Getting Started')


@app.route('/cloud9')
@public
def cloud9():
    html = __load_markdown('static/md/cloud9.md')
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


@app.route('/readme/secret')
@public
def secret_readme():
    return redirect(url_for('readme'))


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
