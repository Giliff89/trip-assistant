from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from model import User, Activity, Restaurant, RestaurantRec, ActivityRec
from model import db, connect_to_db

import random

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_recommendation(location, term):
    """Use Yelp API to get highly rated recommendations"""

    # the sort: 2 gives the highest rated options on Yelp
    params = {"term": term, "sort": "2", "limit": 40}

    recommendations = client.search(location, **params)

    results = {}

    index = 0

    while index < 40:

        results[(recommendations.businesses[index].name).encode(
            'utf-8')] = {"name": (recommendations.businesses[index].name).encode('utf-8'),
                         "rating": float(recommendations.businesses[index].rating),
                         "yelp": (recommendations.businesses[index].url).encode('utf-8'),
                         "business_id": (recommendations.businesses[index].id).encode('utf-8'),
                         "categories": (recommendations.businesses[index].categories)}
        index += 1

    recommendation = random.choice(results.keys())

    name = results[recommendation]["name"]
    rating = results[recommendation]["rating"]
    yelp = results[recommendation]["yelp"]

    business_id = results[recommendation]["business_id"]
    categories = results[recommendation]["categories"]

    result = [name, rating, yelp, business_id, categories]

    return result


def add_act_rec_to_db(activity_id, trip_id):
    """Add the activity to the ActivityRec table under users' trip_id"""

    saved_rec = ActivityRec(activity_id=activity_id,
                            trip_id=trip_id)

    db.session.add(saved_rec)
    db.session.commit()


def add_rest_rec_to_db(restaurant_id, trip_id):
    """Add the restaurant to the RestaurantRec table under users' trip_id"""

    saved_rec = RestaurantRec(restaurant_id=restaurant_id,
                              trip_id=trip_id)

    db.session.add(saved_rec)
    db.session.commit()


def confirm_activity_in_db(name, rating, location, yelp, business_id):
    """Check to see if a rec is saved in the Activity table, and add if not"""

    try:
        db.session.query(Activity.activity_id).filter_by(business_id=business_id).one()

    except:
        new_activity = Activity(name=name,
                                rating=rating,
                                location=location,
                                yelp=yelp,
                                business_id=business_id)

        db.session.add(new_activity)
        db.session.commit()


def confirm_restaurant_in_db(name, rating, location, yelp, business_id):
    """Check to see if a rec is saved in the Restaurant table, and add if not"""

    try:
        db.session.query(Restaurant.restaurant_id).filter_by(business_id=business_id).one()

    except:
        new_restaurant = Restaurant(name=name,
                                    rating=rating,
                                    location=location,
                                    yelp=yelp,
                                    business_id=business_id)

        db.session.add(new_restaurant)
        db.session.commit()


def check_user(username):
    """Comparing username in database to user entry.

    >>> check_user("LunaLiterally")
    True
    >>> check_user("NotaUsername")
    False
    """

    in_db = User.query.filter_by(username=username)

    if in_db.all():
        return True
    else:
        return False


def check_login(username, password):
    """Comparing username and password in database to user entry.

    >>> check_login("LunaLiterally", "isBestDog")
    1
    >>> check_login("Gina89", "Mypass")
    6
    >>> check_login("Thisisdefinitely", "notaUser")
    False
    """

    auth = User.query.filter_by(username=username, password=password).first()

    if auth:
        return auth.user_id
    else:
        return False


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
