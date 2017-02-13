import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from model import User, Trip, Recommendation, Activity, Restaurant

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_restaurants(location):
    """Use Yelp API to get restaurants"""

    params = {"term": "food"}

    request = client.search(location, **params)

    restaurants = {}

    index = 0

    while index < 10:
        restaurants[str(request.businesses[index].name)] = request.businesses[index].rating
        index += 1

    print restaurants


def get_activities(location):
    """Use Yelp API to get activities"""

    params = {"term": "activity"}

    request = client.search(location, **params)

    activities = {}

    index = 0

    while index < 10:
        activities[str(request.businesses[index].name)] = request.businesses[index].rating
        index += 1

    print activities


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
