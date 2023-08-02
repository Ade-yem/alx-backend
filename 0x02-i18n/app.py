#!/usr/bin/env python3
"""Basic Babel setup"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from pytz import timezone
import pytz
from typing import Union, Dict
from datetime import datetime
from datetime import timezone as tmzone
import locale

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Config class for Babel"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Get locale language code"""
    locale = request.args.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user:
        locale = g.user.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale
    locale = request.headers.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Get timezone"""
    tzone = request.args.get('timezone', None)
    if tzone:
        try:
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        tzone = g.user.get('timezone')
        if tzone:
            try:
                return timezone(tzone).zone
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Get user from users"""
    login = request.args.get('login_as', None)
    if login and int(login) in users:
        return users.get(int(login))
    return None


@app.before_request
def before_request():
    """Find a user if any, and set it as a global on flask.g.user"""
    g.user = get_user()
    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))
    fmt = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(fmt)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
      - template 0-index.html
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
