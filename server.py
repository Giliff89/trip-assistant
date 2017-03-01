from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

import funcs

from model import db, connect_to_db
from model import User, Trip, Activity, Restaurant

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

    if funcs.check_user(username) is False:
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id

        flash("Logged in")
        return redirect("/profile/%s" % new_user.user_id)
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

        user = funcs.check_login(username, password)

        if user is False:
            user_in_db = funcs.check_user(username)

            if user_in_db is False:
                flash("There is no user by that username")
                return redirect("/login")
            # If the username is in the db but doesn't match password
            else:
                flash("the password does not match the username")
                return redirect("/login")

        session["user_id"] = user

        flash("Logged in")
        return redirect("/profile/%s" % user)


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

    term = "restaurant"

    restaurant = funcs.get_recommendation(location, term)

    name = restaurant[0]
    rating = restaurant[1]
    yelp = restaurant[2]
    business_id = restaurant[3]
    categories = restaurant[4]

    funcs.confirm_restaurant_in_db(name, rating, location, yelp, business_id)

    return jsonify({"name": name, "rating": rating,
                    "yelp": yelp, "business_id": business_id,
                    "categories": categories})


@app.route('/get_activity_rec', methods=['GET', 'POST'])
def get_activity_rec():
    """Show an activity recommendation for the users' trip"""

    location = request.args.get("location")

    term = "activity"

    activity = funcs.get_recommendation(location, term)

    name = activity[0]
    rating = activity[1]
    yelp = activity[2]
    business_id = activity[3]
    categories = activity[4]

    funcs.confirm_activity_in_db(name, rating, location, yelp, business_id)

    return jsonify({"name": name, "rating": rating,
                    "yelp": yelp, "business_id": business_id,
                    "categories": categories})


@app.route('/save_rest_rec', methods=['POST'])
def save_restaurant_rec_to_db():
    """Ajax route to save restaurant recommendation to trip_id"""

    trip_id = request.form.get("trip_id")
    business_id = request.form.get("business_id")

    restaurant = db.session.query(Restaurant.restaurant_id).filter_by(business_id=business_id).all()

    restaurant_id = restaurant[0][0]

    funcs.add_rest_rec_to_db(restaurant_id, trip_id)

    return jsonify({"trip_id": trip_id, "restaurant_id": restaurant_id})


@app.route('/save_act_rec', methods=['POST'])
def save_activity_rec_to_db():
    """Ajax route to save activity recommendation to trip_id"""

    trip_id = request.form.get("trip_id")
    business_id = request.form.get("business_id")

    activity = db.session.query(Activity.activity_id).filter_by(business_id=business_id).all()

    activity_id = activity[0][0]

    funcs.add_act_rec_to_db(activity_id, trip_id)

    return jsonify({"trip_id": trip_id, "activity_id": activity_id})


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
