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


def get_restaurant(location):
    """Use Yelp API to get highly rated restaurants"""

    params = {"term": "food", "sort": "2", "limit": 40}

    restaurants = client.search(location, **params)

    results = {}

    index = 0

    while index < 40:

        results[(restaurants.businesses[index].name).encode(
            'utf-8')] = {"name": (restaurants.businesses[index].name).encode('utf-8'),
                         "rating": float(restaurants.businesses[index].rating),
                         "yelp": (restaurants.businesses[index].url).encode('utf-8'),
                         "business_id": (restaurants.businesses[index].id).encode('utf-8')}
        index += 1

    restaurant = random.choice(results.keys())

    name = results[restaurant]["name"]
    rating = results[restaurant]["rating"]
    yelp = results[restaurant]["yelp"]

    business_id = results[restaurant]["business_id"]

    result = [name, rating, yelp, business_id]

    return result


def get_activity(location):
    """Use Yelp API to get highly rated activities"""

    params = {"term": "activity", "sort": "2", "limit": 40}

    activities = client.search(location, **params)

    results = {}

    index = 0

    while index < 40:

        results[(activities.businesses[index].name).encode(
            'utf-8')] = {"name": (activities.businesses[index].name).encode('utf-8'),
                         "rating": float(activities.businesses[index].rating),
                         "yelp": (activities.businesses[index].url).encode('utf-8'),
                         "business_id": (activities.businesses[index].id).encode('utf-8')}
        index += 1

    activity = random.choice(results.keys())

    name = results[activity]["name"]
    rating = results[activity]["rating"]
    yelp = results[activity]["yelp"]
    business_id = results[activity]["business_id"]

    result = [name, rating, yelp, business_id]

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
    """Comparing username in database to user entry."""

    in_db = User.query.filter_by(username=username)

    if in_db.all():
        return True
    else:
        return False


def check_login(username, password):
    """Comparing username and password in database to user entry."""

    auth = User.query.filter_by(username=username, password=password)

    if auth.all():
        return auth.all().user_id
    else:
        return False
