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


class Trip(db.Model):
    """Trip information which maps to user_id."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    days = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(128), nullable=False)
    # location as a city for Yelp search capability

    user = db.relationship('User', backref=db.backref('trips'))

    activities = db.relationship("Activity",
                                 secondary="activity_recs")

    restaurants = db.relationship("Restaurant",
                                  secondary="restaurant_recs")


class Activity(db.Model):
    """Single activity recommendation."""

    __tablename__ = "activities"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Activity activity_id=%s name=%s>" % (self.activity_id, self.name)

    activity_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(80), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    business_id = db.Column(db.String(256), nullable=False)

    trips = db.relationship("Trip",
                            secondary="activity_recs")


class Restaurant(db.Model):
    """Single restaurant recommendation."""

    __tablename__ = "restaurants"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant restaurant_id=%s name=%s>" % (self.restaurant_id, self.name)

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(80), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    business_id = db.Column(db.String(256), nullable=False)

    trips = db.relationship("Trip",
                            secondary="restaurant_recs")


# Association table for restaurant recommendations to trip
class RestaurantRec(db.Model):
    """One restaurant recommendation for a trip."""

    __tablename__ = "restaurant_recs"

    rest_rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)

    trip = db.relationship("Trip", backref=db.backref("restaurant_assoc"))
    restaurant = db.relationship("Restaurant", backref=db.backref("trip_assoc"))


# Association table for activity recommendations to trip
class ActivityRec(db.Model):
    """One activity recommendation for a trip."""

    __tablename__ = "activity_recs"

    act_rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)
    activity_id = db.Column(db.Integer,
                            db.ForeignKey('activities.activity_id'),
                            nullable=False)

    trip = db.relationship("Trip", backref=db.backref("activity_assoc"))
    activity = db.relationship("Activity", backref=db.backref("trip_assoc"))


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
