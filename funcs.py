from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from model import User, Activity, Restaurant  # Recommendation, Trip
from model import db, connect_to_db

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)

# TODO - turn these functions into one, set up ajax to determine the term to use


def get_restaurants(location, result_num):
    """Use Yelp API to get highly rated restaurants"""

    # the sort=2 gives the highest rated/reviewed restaurants
    params = {"term": "food", "sort": "2"}

    request = client.search(location, **params)

    restaurants = {}

    index = 0

    while index < result_num:

        restaurants[(request.businesses[index].name).encode('utf-8')] = {"name": (request.businesses[index].name).encode('utf-8'),
                                                                         "rating": float(request.businesses[index].rating),
                                                                         "yelp": (request.businesses[index].url).encode('utf-8'),
                                                                         "business_id": (request.businesses[index].id).encode('utf-8')}
        index += 1

    for business in restaurants:

        name = restaurants[business]["name"]
        rating = restaurants[business]["rating"]
        yelp = restaurants[business]["yelp"]
        business_id = restaurants[business]["business_id"]

        new_restaurant = Restaurant(name=name,
                                    rating=rating,
                                    location=location,
                                    yelp=yelp,
                                    business_id=business_id)

        db.session.add(new_restaurant)
        db.session.commit()


def get_activities(location, result_num):
    """Use Yelp API to get highly rated activities"""

    # the sort=2 gives the highest rated/reviewed activities
    params = {"term": "activity", "sort": "2"}

    request = client.search(location, **params)

    activities = {}

    index = 0

    while index < result_num:
        # TODO - add in .encode()
        activities[(request.businesses[index].name).encode('utf-8')] = {"name": (request.businesses[index].name).encode('utf-8'),
                                                                        "rating": float(request.businesses[index].rating),
                                                                        "yelp": (request.businesses[index].url).encode('utf-8'),
                                                                        "business_id": (request.businesses[index].id).encode('utf-8')}
        index += 1

    for business in activities:

        name = activities[business]["name"]
        rating = activities[business]["rating"]
        yelp = activities[business]["yelp"]
        business_id = activities[business]["business_id"]

        new_activity = Activity(name=name,
                                rating=rating,
                                location=location,
                                yelp=yelp,
                                business_id=business_id)

        db.session.add(new_activity)
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
