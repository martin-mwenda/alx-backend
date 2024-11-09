#!/usr/bin/env python3
'''Basic Flask app with Babel integration for language configuration.'''

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    '''Configuration for Flask-Babel with language, locale,
    and timezone settings.'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

# Initialize Babel for localization
babel = Babel(app)


@app.route('/')
def index():
    '''Renders the homepage.'''
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(debug=True)
