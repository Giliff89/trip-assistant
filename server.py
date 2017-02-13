from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from funcs import check_user, check_login
from model import db, connect_to_db
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

    # pass in location as arguement/in search

    request = client.search('San Francisco', **params)

    # Next step try out different data types I can pull with this, and create
    # dictionaries within a main dictionary. This will let me store the info I need
    # for my tables. Check categories, business ids, urls for business and yelp

    restaurants = {}

    index = 0

    while index < 10:
        restaurants[str(request.businesses[index].name)] = request.businesses[index].rating
        index += 1

    print restaurants
    # I need to be able to set the categories to do a search for
    # activities, and a search for food. I also need to set the limit to return 1 result
    # in each category per day of a trip


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
        return redirect("/profile/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/profile/<user_id>')
def get_user_profile(user_id):
    """brings user to their profile page when logged in"""

    user = User.query.get(user_id)

    return render_template("user_profile.html", user=user)


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
        location = request.form['location']
        num_days = request.form['days']
        user_id = session['user_id']

        new_trip = Trip(location=location, days=num_days, user_id=user_id)

        db.session.add(new_trip)
        db.session.commit()
        flash('Your trip has been successfully added!')
        return redirect('/trip_profile/%s/%s' % (new_trip.trip_id, new_trip.location))


@app.route('/trip_profile/<trip_id>/<location>')
def trip_profile(trip_id, location):
    """Displays trip information and recommendations for user's specific trip"""

    trip = Trip.query.get(trip_id)

    return render_template('trip_page.html', trip=trip)


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
