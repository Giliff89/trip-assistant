from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)


app.secret_key = "ufiwehf9823rbfqbuef32hfbbc9s8398523rvbfiw"
#  for Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")
