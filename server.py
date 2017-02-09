from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import check_user, check_login, db, connect_to_db
from model import User, Trip, Recommendation, Activity, Restaurant

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import json

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
#  for Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_results(params):
    """Use Yelp API to search using the parameters from the user selected terms"""

    request = client.search('San Francisco', **params)

#   # Turn the JSON response into a Python dictionary
    data = request.businesses[0].name, request.businesses[1].name, request.businesses[2].name, request.businesses[3].name

    # return data
    print data
    # print request.businesses[0].name, request.businesses[1].name
    # return request.businesses

    # Search is working, now I need to be able to set the categories to do a search for
    # activities, and a search for food. I also need to set the limit to return 1 result
    # in each category per day of a trip

    # ALSO: Need to be able to pull the data into a python dictionary


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

    username = request.form['username']
    password = request.form['password']

    new_user = User(username=username, password=password)

    if check_user(username) is False:
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        flash('That username is taken, choose a new username or login')
        return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Checks if login credentials match database"""

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("There is no user by that username")
            return redirect("/login")

        if user.password != password:
            flash("the password does not match the username")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("Logged in")
        return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/users')
def get_user_profile():
    """brings user to their profile page when logged in"""

    return render_template("user_profile.html")


# @app.route('/preferences', methods=["GET", "POST"])
# def user_preferences():
#     """User chooses 5 terms to define their travel preferences"""

#     if request.method == "GET":
#         return render_template("personality_quiz.html")
#     else:
#         pass  # need to add the post in for user preferences


@app.route('/add_trip', methods=["GET", "POST"])
def user_trip():
    """Allows user to add a trip to their profile"""

    if request.method == "GET":
        return render_template("add_trip.html")
    else:
        pass  # need to add the post in for user trip


# @app.route('/recommendations')
# def get_recs():
#     """Search Yelp for trip recommendations"""

#     term = request.args.get("term")

#     search database

#     return jsonify(results)


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
