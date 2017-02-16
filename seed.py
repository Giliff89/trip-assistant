# This file will seed my database with data on restaurants and activities by city

from sqlalchemy import func

from model import User, Trip, Activity, Restaurant, RestaurantRec, ActivityRec
from model import connect_to_db, db

from server import app


def load_users():
    """Load users into database"""

    print "Users loading"

    # To make sure we won't be trying to add duplicate users
    User.query.delete()

    for row in open("seed_data/users.csv"):
        row = row.rstrip()
        user_id, username, password = row.split(",")

        user = User(user_id=user_id,
                    username=username,
                    password=password)

        db.session.add(user)

    db.session.commit()


def load_trips():
    """Load trips into database"""

    print "Trips loading"

    Trip.query.delete()

    for row in open("seed_data/trips.csv"):
        row = row.rstrip()
        trip_id, user_id, days, location = row.split(",")

        trip = Trip(trip_id=trip_id,
                    user_id=user_id,
                    days=days,
                    location=location)

        db.session.add(trip)

    db.session.commit()


def load_activities():
    """Load activities into database"""

    print "Activities loading"

    Activity.query.delete()

    for row in open("seed_data/activities.csv"):
        row = row.rstrip()
        activity_id, name, rating, location, yelp, business_id = row.split(",")

        activity = Activity(activity_id=activity_id,
                            name=name,
                            rating=rating,
                            location=location,
                            yelp=yelp,
                            business_id=business_id)

        db.session.add(activity)

    db.session.commit()


def load_restaurants():
    """Load restaurants into database"""

    print "Restaurants loading"

    Restaurant.query.delete()

    for row in open("seed_data/restaurants.csv"):
        row = row.rstrip()
        restaurant_id, name, rating, location, yelp, business_id = row.split(",")

        restaurant = Restaurant(restaurant_id=restaurant_id,
                                name=name,
                                rating=rating,
                                location=location,
                                yelp=yelp,
                                business_id=business_id)

        db.session.add(restaurant)

    db.session.commit()


def load_restaurant_recs():
    """Load resaturant recs into database"""

    print "Restaurant recommendations loading"

    RestaurantRec.query.delete()

    for row in open("seed_data/restaurant_recs.csv"):
        row = row.rstrip()
        rest_rec_id, trip_id, restaurant_id = row.split(",")

        rest_rec = RestaurantRec(rest_rec_id=rest_rec_id,
                                 trip_id=trip_id,
                                 restaurant_id=restaurant_id)

        db.session.add(rest_rec)

    db.session.commit()


def load_activity_recs():
    """Load activity recs into database"""

    print "Activity recommendations loading"

    ActivityRec.query.delete()

    for row in open("seed_data/activity_recs.csv"):
        row = row.rstrip()
        act_rec_id, trip_id, activity_id = row.split(",")

        act_rec = ActivityRec(act_rec_id=act_rec_id,
                              trip_id=trip_id,
                              activity_id=activity_id)

        db.session.add(act_rec)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_trip_id():
    """Set value for the next trip_id after seeding database"""

    result = db.session.query(func.max(Trip.trip_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('trips_trip_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_restaurant_id():
    """Set value for the next restaurant_id after seeding database"""

    result = db.session.query(func.max(Restaurant.restaurant_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('restaurants_restaurant_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_activity_id():
    """Set value for the next activity_id after seeding database"""

    result = db.session.query(func.max(Activity.activity_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('activities_activity_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_restaurant_rec_id():
    """Set value for the next rest_rec_id after seeding database"""

    result = db.session.query(func.max(RestaurantRec.rest_rec_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('restaurant_recs_rest_rec_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_activity_rec_id():
    """Set value for the next act_rec_id after seeding database"""

    result = db.session.query(func.max(ActivityRec.act_rec_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('activity_recs_act_rec_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_users()
    load_trips()
    load_activities()
    load_restaurants()
    load_restaurant_recs()
    load_activity_recs()
    set_val_user_id()
    set_val_trip_id()
    set_val_restaurant_id()
    set_val_activity_id()
    set_val_restaurant_rec_id()
    set_val_activity_rec_id()
