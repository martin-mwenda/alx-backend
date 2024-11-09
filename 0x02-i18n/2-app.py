#!/usr/bin/env python3
'''Task 2: Get locale from request
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    '''Configuration class for Flask app with localization settings.'''

    DEBUG = True  # Enable Flask debugging
    LANGUAGES = ["en", "fr"]  # Supported languages
    BABEL_DEFAULT_LOCALE = "en"  # Default locale if no match is found
    BABEL_DEFAULT_TIMEZONE = "UTC"  # Default timezone


# Initialize Flask app and load configuration
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False  # Allow flexible URL patterns without

# Initialize Flask-Babel for localization
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Determines the best locale match for the web page.

    This function checks the request's Accept-Language header and
    returns the best match from the available languages configured in the app.

    Returns:
        str: The best matched locale (language code).
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''Renders the homepage.

    This route renders the homepage, allowing for localization based
    on the selected locale.

    Returns:
        html: The homepage template.
    '''
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
