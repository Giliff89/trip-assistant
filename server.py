from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from secrets import SECRET_KEY


app = Flask(__name__)


app.secret_key = SECRET_KEY
#  for Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def registration():
    """Allows user to register for an account"""

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def process_registration():
    """Redirects user to the homepage if the username is not taken"""

    # username = request.form.get('username')
    # email = request.form.get('email')
    # password = request.form.get('password')

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
