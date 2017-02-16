# This file will seed my database with data on restaurants and activities by city

from sqlalchemy import func

from model import User, Trip, Activity, Restaurant  # Recommendation
from model import connect_to_db, db

from server import app


def load_users():
    """Load users into database"""

    print "Users"

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

    print "Trips"

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

    print "Activities"

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

    print "Restaurants"

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


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_users()
    load_trips()
    # # load_recommendations()
    load_activities()
    load_restaurants()
    set_val_user_id()
    set_val_trip_id()
    set_val_restaurant_id()
    set_val_activity_id()
