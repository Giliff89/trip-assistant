from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from secrets import SECRET_KEY

from model import check_user, check_login


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


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Checks if login credentials match database"""

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if check_user(username) is True:
            authenticate = check_user(username, password)
            if authenticate:
                session['user'] = authenticate
                flash('Login successful')
                return redirect('/')
            else:
                flash('The password did not match the username')
        else:
            return redirect('/register')



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
