from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from server import app

from model import User, Trip, Activity, Restaurant
from model import db, connect_to_db

from seed import set_val_restaurant_id, set_val_activity_id

import random

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


# def get_restaurants(location, result_num):
#     """Use Yelp API to get highly rated restaurants"""

#     params = {"term": "food", "sort": "2"}

#     request = client.search(location, **params)

#     restaurants = {}

#     index = 0

#     while index < result_num:

#         restaurants[(request.businesses[index].name).encode('utf-8')] = {"name": (request.businesses[index].name).encode('utf-8'),
#                                                                          "rating": float(request.businesses[index].rating),
#                                                                          "yelp": (request.businesses[index].url).encode('utf-8'),
#                                                                          "business_id": (request.businesses[index].id).encode('utf-8')}
#         index += 1

#         set_val_restaurant_id()

#     for business in restaurants:

#         name = restaurants[business]["name"]
#         rating = restaurants[business]["rating"]
#         yelp = restaurants[business]["yelp"]
#         business_id = restaurants[business]["business_id"]

#         new_restaurant = Restaurant(name=name,
#                                     rating=rating,
#                                     location=location,
#                                     yelp=yelp,
#                                     business_id=business_id)

#         db.session.add(new_restaurant)
#     db.session.commit()


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

    print name, rating, yelp, business_id


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

    print name, rating, yelp, business_id


# def get_activities(location, result_num):
#     """Use Yelp API to get highly rated activities"""

#     params = {"term": "activity", "sort": "2"}

#     request = client.search(location, **params)

#     activities = {}

#     index = 0

#     while index < result_num:
#         activities[(request.businesses[index].name).encode('utf-8')] = {"name": (request.businesses[index].name).encode('utf-8'),
#                                                                         "rating": float(request.businesses[index].rating),
#                                                                         "yelp": (request.businesses[index].url).encode('utf-8'),
#                                                                         "business_id": (request.businesses[index].id).encode('utf-8')}
#         index += 1

#         set_val_activity_id()

#     for business in activities:

#         name = activities[business]["name"]
#         rating = activities[business]["rating"]
#         yelp = activities[business]["yelp"]
#         business_id = activities[business]["business_id"]

#         new_activity = Activity(name=name,
#                                 rating=rating,
#                                 location=location,
#                                 yelp=yelp,
#                                 business_id=business_id)

#         print new_activity.name

#         db.session.add(new_activity)
#     db.session.commit()


connect_to_db(app)
