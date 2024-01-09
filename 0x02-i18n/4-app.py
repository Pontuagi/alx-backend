#!/usr/bin/env python3

"""
Basic Babel setup module
"""

from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """
    Configuration class setting up available languages and
    default locale/timezone for Babel.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """Selects the language based on the client's preferences."""
    if 'locale' in request.args and request.args[
            'locale'] in app.config['LANGUAGES']:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Renders the index template."""
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
