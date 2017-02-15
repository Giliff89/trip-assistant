from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of Trip Assistant website."""

    __tablename__ = "users"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(32),
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(32), nullable=False)

    # Add in a term table for personalization later

    # For number indicating string length, assign to a constant to give context


class Trip(db.Model):
    """Trip information which maps to user_id."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    days = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(128), nullable=False)
    # location as a city for Yelp search capability

    user = db.relationship('User', backref=db.backref('trips'))

# Make 2 association tables, one for restaurant and one for activity

# Association table
# Instead, make this connection take in a restaurant or activity id, and link it to a trip id.
# class Recommendation(db.Model):
#     """One day of recommendations for a trip."""

#     __tablename__ = "recommendations"

#     rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     trip_id = db.Column(db.Integer,
#                         db.ForeignKey('trips.trip_id'),
#                         nullable=False)
    # restaurant_id = db.Column(db.Integer,
    #                           db.ForeignKey('restaurants.restaurant_id'),
    #                           nullable=False)
    # activity_id = db.Column(db.Integer,
    #                         db.ForeignKey('activities.activity_id'),
    #                         nullable=False)

    # trip = db.relationship('Trip', backref=db.backref('recommendations'))

    # restaurant = db.relationship('Restaurant',
    #                              foreign_keys=[restaurant_id],
    #                              backref=db.backref('recommendation'))
    # activity = db.relationship('Activity',
    #                            foreign_keys=[activity_id],
    #                            backref=db.backref('recommendation'))

    # Rather than have a rec table linking the recs to trips, have an association table that
    # will allow me to save the trip_id and rec_id each time a button is pressed.

# Can join the shared data on these two tables, have activity specific data in activity table


class Activity(db.Model):
    """Single activity recommendation."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(80), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    business_id = db.Column(db.String(256), nullable=False)

    # Add access methods and queries in here

# Testing out github branching!

class Restaurant(db.Model):
    """Single restaurant recommendation."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(80), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    business_id = db.Column(db.String(256), nullable=False)

# Can separate each table into a new document with methods associated with that table


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recommendations'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
