# This file will seed my database with data on restaurants and activities by city
# File is currently in progress! Lots of placeholders for now

from sqlalchemy import func

from model import User, Trip, Recommendation, Activity, Restaurant
from model import connect_to_db, db

from server import app


def load_users():
    """Load users into database"""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    # User.query.delete()

    # Read file and insert data
    # for row in open(file_name):
    #     row = row.rstrip()
    #     user_id, username, password, q1_term, q2_term, q3_term, q4_term, q5_term = row.split("|")

    #     user = User(user_id=user_id,
    #                 username=username,
    #                 password=password)

    #     db.session.add(user)

    # db.session.commit()


def load_trips():
    """Load trips into database"""

    print "Trips"


def load_recommendations():
    """Load recommendations into database"""

    print "Recommendations"


def load_activities():
    """Load activities into database"""

    print "Activities"


def load_restaurants():
    """Load restaurants into database"""

    print "Restaurants"


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import all of the different types of data
    # load_users()
    # load_trips()
    # load_recommendations()
    # load_activities()
    # load_restaurants()
    set_val_user_id()
