from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from funcs import check_user, check_login  # get_activities, get_restaurants
from model import db, connect_to_db
from model import User, Trip, Activity, Restaurant, RestaurantRec, ActivityRec

# from seed import set_val_restaurant_rec_id, set_val_activity_rec_id

import random

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
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

        # Can condense this with check_user and check_login functions


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


@app.route('/add_trip', methods=["GET", "POST"])
def user_trip():
    """Allows user to add a trip to their profile"""

    if request.method == "GET":
        return render_template("add_trip.html")
    else:
        location = request.form['location']
        user_id = session['user_id']

        new_trip = Trip(location=location, user_id=user_id)

        db.session.add(new_trip)
        db.session.commit()
        flash('Your trip has been successfully added!')
        return redirect('/trip_profile/%s/%s' % (new_trip.trip_id, new_trip.location))


@app.route('/trip_profile/<trip_id>/<location>')
def trip_profile(trip_id, location):
    """Displays trip information and recommendations for user's specific trip"""

    trip = Trip.query.get(trip_id)

    return render_template('trip_page.html',
                           trip=trip)


@app.route('/get_restaurant_rec', methods=['GET', 'POST'])
def get_restaurant_rec():
    """Show a restaurant recommendation for the users' trip"""

    location = request.args.get("location")

    rest_query = random.choice(db.session.query(Restaurant.name,
                                                Restaurant.rating,
                                                Restaurant.yelp).filter(
        location == Restaurant.location).all())

    return jsonify({"name": rest_query[0], "rating": rest_query[1], "yelp": rest_query[2]})

    # set_val_restaurant_rec_id()

    #     name = recommendation.name
    #     rating = recommendation.rating
    #     yelp = recommendation.yelp

    #     new_rec = RestaurantRec(trip_id=trip_id,
    #                             restaurant_id=recommendation.restaurant_id)

    #     db.session.add(new_rec)
    # db.session.commit()

    # return recommendation


@app.route('/get_activity_rec', methods=['GET', 'POST'])
def get_activity_rec():
    """Show an activity recommendation for the users' trip"""

    location = request.args.get("location")

    act_query = random.choice(db.session.query(Activity.name,
                                               Activity.rating,
                                               Activity.yelp).filter(
        location == Activity.location).all())

    return jsonify({"name": act_query[0], "rating": act_query[1], "yelp": act_query[2]})

    # set_val_activity_rec_id()

    #     name = recommendation.name
    #     rating = recommendation.rating
    #     yelp = recommendation.yelp

    #     new_rec = ActivityRec(trip_id=trip_id,
    #                             activity_id=recommendation.activity_id)

    #     db.session.add(new_rec)
    # db.session.commit()

    # return recommendation


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
