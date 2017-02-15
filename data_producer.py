from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from server import app

from model import User, Trip, Activity, Restaurant  # Recommendation
from model import db, connect_to_db

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_restaurants(location, days):
    """Use Yelp API to get highly rated restaurants"""

    params = {"term": "food", "sort": "2"}

    request = client.search(location, **params)

    restaurants = {}

    index = 0

    while index < days:
        try:
            restaurants[str(request.businesses[index].name)] = {"name": str(request.businesses[index].name),
                                                                "rating": float(request.businesses[index].rating),
                                                                "yelp": str(request.businesses[index].url),
                                                                "business_id": str(request.businesses[index].id)}
            index += 1

        except UnicodeEncodeError:
            restaurants[(request.businesses[index].name).encode('utf-8')] = {"name": (request.businesses[index].name).encode('utf-8'),
                                                                             "rating": float(request.businesses[index].rating),
                                                                             "yelp": str(request.businesses[index].url),
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


def get_activities(location, days):
    """Use Yelp API to get highly rated activities"""

    params = {"term": "activity", "sort": "2"}

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

        new_activity = Activity(name=name,
                                rating=rating,
                                location=location,
                                yelp=yelp,
                                business_id=business_id)

        db.session.add(new_activity)
        db.session.commit()


connect_to_db(app)
