from flask import (
    request, g, current_app,
    render_template, redirect, url_for, flash,
)

from flask.ext.login import (
    LoginManager,
    login_user, logout_user, current_user
)


from lib.log import get_logger
from lib.models.team import Team
from lib.server import app, form_error
from lib.forms import LoginForm

import settings.secrets


app.secret_key = settings.secrets.SESSION_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logger = get_logger(__name__)


@app.before_request
def load_users():

    # You should know what you're doing if you're using this
    # This will leave the request context team as None, which will break shit
    override_auth_check = 'X-Override-Auth' in request.headers and \
            request.headers['X-Override-Auth'] == settings.secrets.OVERRIDE_AUTH_HEADER

    if not current_user.is_authenticated and not is_public() and not override_auth_check:
        app.logger.info('no auth, redirecting')
        return login_manager.unauthorized()

    if is_admin_only() and not current_user.type == Team.TYPE_ADMIN:
        return "You do not have access", 403

    g.team = current_user


def public(func):
    """
    Decorator that marks a route as not needing authentication.
    This needs to wrap the inner function, or it won't take effect, e.g.

    @app.route(...)
    @public
    def route...
    """
    func._public = True
    return func


def is_public():
    """Returns True if the current route is public, False otherwise """

    # static files are always public
    if request.endpoint == 'static':
        return True

    endpoint = current_app.view_functions.get(request.endpoint)
    if not endpoint:
        return True

    return getattr(endpoint, '_public', False)


def admin_only(func):
    """
    Decorator that marks a route as only accessable to admins.
    This needs to wrap the inner function, or it won't take effect, e.g.

    @app.route(...)
    @admin_only
    def route...
    """
    func._admin_only = True
    return func


def is_admin_only():
    """Returns True if the current route is only avail to admins, False otherwise """
    endpoint = current_app.view_functions.get(request.endpoint)
    if not endpoint:
        return False

    return getattr(endpoint, '_admin_only', False)


@login_manager.user_loader
def load_team(id):
    """Given id, return the associated Team object.

    :param id: team to retrieve
    """
    return Team.find_one({'_id': id})


@app.route('/login', methods=['GET', 'POST'])
@public
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_paths'))

    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('auth/login.html', form=form)

    email = form.email.data
    password = form.password.data

    team = Team.find_one({'member_emails': email})

    if team and team.check_password(password):
        login_user(team)

        default_next = url_for('list_teams') if team.type == Team.TYPE_ADMIN else url_for('app_paths')
        return redirect(request.values.get('next') or default_next)
    else:
        return form_error('Bad email or password')


@app.route("/logout")
@public
def logout():
    if current_user.is_authenticated:
        flash('You have been logged out')
        logout_user()
    return redirect(url_for('login'))
