from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import check_user, check_login, db, connect_to_db
from model import User, Trip, Recommendation, Activity, Restaurant

# import rauth

app = Flask(__name__)


app.secret_key = 'SECRET_KEY'
#  for Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined


# def get_results(params):
# """Use Yelp API to search using the parameters from the user selected terms"""

#   session = rauth.OAuth1Session(consumer_key='CONSUMER_KEY',
#                                 consumer_secret='CONSUMER_SECRET',
#                                 token_key='TOKEN',
#                                 token_secret='TOKEN_SECRET')

#   request = session.get("http://api.yelp.com/v3/businesses/search",params=params)

#   Turn the JSON response into a Python dictionary
#   data = request.json()
#   session.close()

#   return data

# Reading about how to use yelp API
# need to learn more about and pip install rauth to handle OAuth stuff


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


@app.route('/quiz', methods=["GET", "POST"])
def user_preferences():
    """User takes a 5 question quiz to defin their travel preferences"""

    if request.method == "GET":
        return render_template("personality_quiz.html")
    else:
        pass  # need to add the post in for user preferences


@app.route('/add_trip', methods=["GET", "POST"])
def user_trip():
    """Allows user to add a trip to their profile"""

    if request.method == "GET":
        return render_template("add_trip.html")
    else:
        pass  # need to add the post in for user trip


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
