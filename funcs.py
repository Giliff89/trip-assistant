from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from model import User, Trip, Recommendation, Activity, Restaurant
from model import db, connect_to_db

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_restaurants(location, days):
    """Use Yelp API to get highly rated restaurants"""

    params = {"term": "food", "sort": "2"}
    # the sort=2 gives the highest rated/reviewed restaurants

    request = client.search(location, **params)

    restaurants = {}

    index = 0

    while index < days:
        restaurants[str(request.businesses[index].name)] = {"name": str(request.businesses[index].name),
                                                            "rating": float(request.businesses[index].rating),
                                                            "yelp": str(request.businesses[index].url),
                                                            "business_id": str(request.businesses[index].id)}
        index += 1

    # print restaurants

    for business in restaurants:

        name = restaurants[business]["name"]
        rating = restaurants[business]["rating"]
        yelp = restaurants[business]["yelp"]
        business_id = restaurants[business]["business_id"]

        print name, rating, yelp, business_id

    # Next step is to add them to the db, assigned to their rec_id


def get_activities(location, days):
    """Use Yelp API to get highly rated activities"""

    params = {"term": "activity", "sort": "2"}
    # the sort=2 gives the highest rated/reviewed activities

    request = client.search(location, **params)

    activities = {}

    index = 0

    while index < days:
        activities[str(request.businesses[index].name)] = {"name": str(request.businesses[index].name),
                                                           "rating": float(request.businesses[index].rating),
                                                           "yelp": str(request.businesses[index].url),
                                                           "business_id": str(request.businesses[index].id)}
        index += 1

    for business in activities:

        name = activities[business]["name"]
        rating = activities[business]["rating"]
        yelp = activities[business]["yelp"]
        business_id = activities[business]["business_id"]

        # new_activity = Activity(name=name, rating=rating, yelp=yelp, business_id=business_id, rec_id=100)

        # db.session.add(new_activity)
        # db.session.commit()

        # not set up yet, need to connect to database still
        # print new_activity
        print name, rating, yelp, business_id


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
