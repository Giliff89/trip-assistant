from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from model import User, Activity, Restaurant, RestaurantRec, ActivityRec, Trip
from model import db, connect_to_db

import random

from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.recommenders.knn import UserBasedRecommender
from scikits.crab.metrics import pearson_correlation
from scikits.crab.similarities import UserSimilarity

cred = open('config_secret.json').read()
creds = json.loads(cred)
auth = Oauth1Authenticator(**creds)
client = Client(auth)


def get_custom_rec(user_id, location, term):
    """Pearson correlation to compare to other users and give custom recommendations"""

    users = user_list_setup()

    if term == "restaurant":
        rest_data = rest_data_dict_setup(users)
        converted_data = load_rest_data_dict(rest_data)

        model = MatrixPreferenceDataModel(converted_data)

        similarity = UserSimilarity(model, pearson_correlation)

        recommender = UserBasedRecommender(model, similarity, with_preference=True)

        recommendations = list(recommender.recommend(user_id))

        for rec in recommendations:
            if db.session.query(Restaurant).filter_by(restaurant_id=rec[0], location=location).all():
                return rec[0]

    elif term == "activity":
        act_data = act_data_dict_setup(users)
        converted_data = load_act_data_dict(act_data)

        model = MatrixPreferenceDataModel(converted_data)

        similarity = UserSimilarity(model, pearson_correlation)

        recommender = UserBasedRecommender(model, similarity, with_preference=True)

        recommendations = list(recommender.recommend(user_id))

        for rec in recommendations:
            if db.session.query(Activity).filter_by(activity_id=rec[0], location=location).all():
                return rec[0]

    # output is a list of recommendations. If user has no data,
    # recommendations are sorted by popularity

    # ordered list of restaurant_ids, or activity_ids. Check if it's in the city
    # of the trip. If not, go to the next one and try again


def get_random_rec(location, term):
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
                         "categories": (recommendations.businesses[index].categories),
                         "image_url": str(recommendations.businesses[index].image_url)}
        index += 1

    recommendation = random.choice(results.keys())

    name = results[recommendation]["name"]
    rating = results[recommendation]["rating"]
    yelp = results[recommendation]["yelp"]

    business_id = results[recommendation]["business_id"]
    categories = results[recommendation]["categories"]
    image_url = results[recommendation]["image_url"]

    result = [name, rating, yelp, business_id, categories, image_url]

    return result


def add_act_rec_to_db(activity_id, trip_id, rec_value):
    """Add the activity to the ActivityRec table under users' trip_id"""

    saved_rec = ActivityRec(activity_id=activity_id,
                            trip_id=trip_id,
                            rec_value=rec_value)

    db.session.add(saved_rec)
    db.session.commit()


def add_rest_rec_to_db(restaurant_id, trip_id, rec_value):
    """Add the restaurant to the RestaurantRec table under users' trip_id"""

    saved_rec = RestaurantRec(restaurant_id=restaurant_id,
                              trip_id=trip_id,
                              rec_value=rec_value)

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


def user_list_setup():
    """Set up list of users in database for data arrangement"""
    user_list = []
    users = db.session.query(User.user_id).all()
    for user in users:
        user_list.append(user[0])
    return user_list


def rest_data_dict_setup(user_list):
    """Set up nested dictionary for restaurant pearson correlation"""
    restaurant_data = {}
    for user in user_list:
        if user not in restaurant_data:
            restaurant_data[user] = {}
    return restaurant_data


def act_data_dict_setup(user_list):
    """Set up nested dictionary for activity pearson correlation"""
    activity_data = {}
    for user in user_list:
        if user not in activity_data:
            activity_data[user] = {}
    return activity_data


def load_rest_data_dict(restaurant_data):
    """Load restaurant_id and rec_values into nested dictionary for pearson correlation"""
    for user in restaurant_data:
        trip_list = []
        trips = db.session.query(Trip.trip_id).filter_by(user_id=user).all()
        for trip in trips:
            trip_list.append(trip[0])
        for trip_id in trip_list:
            rest_recs = list(db.session.query(
                RestaurantRec.restaurant_id, RestaurantRec.rec_value).filter_by(
                trip_id=trip_id).all())
            for rec_pair in rest_recs:
                restaurant_data[user][rec_pair[0]] = rec_pair[1]
    return restaurant_data


def load_act_data_dict(activity_data):
    """Load activity_id and rec_values into nested dictionary for pearson correlation"""
    for user in activity_data:
        trip_list = []
        trips = db.session.query(Trip.trip_id).filter_by(user_id=user).all()
        for trip in trips:
            trip_list.append(trip[0])
        for trip_id in trip_list:
            act_recs = list(db.session.query(
                ActivityRec.activity_id, ActivityRec.rec_value).filter_by(
                trip_id=trip_id).all())
            for rec_pair in act_recs:
                activity_data[user][rec_pair[0]] = rec_pair[1]
    return activity_data


def check_location_in_db(location, term):
    """Checks if the location has options in the db to run the Pearson correlation"""

    if term == "restaurant":
        if db.session.query(Restaurant).filter_by(location=location).all():
            return True
    else:
        if db.session.query(Activity).filter_by(location=location).all():
            return True


def get_act_business_id(activity_id):
    """Given the activity_id, get the business_id for a Yelp query"""

    business_id = db.session.query(Activity.business_id).filter_by(
        activity_id=activity_id).first()

    return business_id


def get_rest_business_id(restaurant_id):
    """Given the restaurant_id, get the business_id for a Yelp query"""

    business_id = db.session.query(Restaurant.business_id).filter_by(
        restaurant_id=restaurant_id).first()

    return business_id


def get_info_using_business_id(business_id):
    """When returning a rec from the Pearson correlation, query Yelp for info"""

    print business_id
    response = client.get_business(business_id[0])

    business = response.business

    results = {}

    results = {"name": (business.name).encode('utf-8'),
               "rating": float(business.rating),
               "yelp": (business.url).encode('utf-8'),
               "business_id": (business.id).encode('utf-8'),
               "categories": (business.categories),
               "image_url": str(business.image_url)}

    name = results["name"]
    rating = results["rating"]
    yelp = results["yelp"]

    business_id = results["business_id"]
    categories = results["categories"]
    image_url = results["image_url"]

    result = [name, rating, yelp, business_id, categories, image_url]

    return result


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
