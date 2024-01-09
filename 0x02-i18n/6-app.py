#!/usr/bin/env python3

"""
flask app module
"""


from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext

app = Flask(__name__)


class Config:
    """
    Configuration class for setting up available languages and
    default locale/timezone for Babel.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)

# User mockup database table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Selects the language based on the client's preferences."""
    # Check if a user is logged in and their preferred locale is supported
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # Check for locale in URL parameters
    if 'locale' in request.args and request.args[
            'locale'] in app.config['LANGUAGES']:
        return request.args['locale']

    # Use request header to determine the best match for supported languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    """
    Retrieve user details based on the provided user ID.
    Args:
        user_id (int): ID of the user to retrieve.
    Returns:
        dict or None: User details if found, otherwise None.
    """
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Executed before handling any request.
    Retrieves the user based on the 'login_as' parameter in the URL and
    sets it in the global context 'g'.
    """
    user_id = request.args.get('login_as')
    g.user = None
    if user_id:
        user = get_user(int(user_id))
        if user:
            g.user = user


@app.route('/')
def index():
    """
    Renders the index template and displays a welcome message
    based on user login status.
    """
    welcome_message = gettext(
        "You are logged in as %(username)s."
        ) if g.user else gettext("You are not logged in.")
    return render_template(
        '6-index.html',
        welcome_message=welcome_message,
        user=g.user
        )


if __name__ == '__main__':
    app.run(debug=True)
