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
    rating = db.Column(db.Float, nullable=False)
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
    rating = db.Column(db.Float, nullable=False)
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
    # This column will save a value of 1, 2, or 3 to determine if a user likes,
    # dislikes, or doesn't prefer a recommendation either way. This will be used
    # for my Pearson correlation
    rec_value = db.Column(db.Integer, nullable=False)

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
    # This column will save a value of 1, 2, or 3 to determine if a user likes,
    # dislikes, or doesn't prefer a recommendation either way. This will be used
    # for my Pearson correlation
    rec_value = db.Column(db.Integer, nullable=False)

    trip = db.relationship("Trip", backref=db.backref("activity_assoc"))
    activity = db.relationship("Activity", backref=db.backref("trip_assoc"))


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recommendations'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Create some sample data."""

    user1 = User(username="Testuser", password="Testpass")
    user2 = User(username="Love2go", password="Seetheworld25")
    user3 = User(username="Tr!pping", password="world@large")

    trip1 = Trip(user_id=1, location="San Francisco")
    trip2 = Trip(user_id=3, location="Seattle")
    trip3 = Trip(user_id=1, location="Los Angeles")
    trip4 = Trip(user_id=2, location="Kona")

    act1 = Activity(name="Funtime", rating=5, location="Seattle",
                    yelp="www.funtime-seattle.com", business_id="Funtime-Seattle")
    act2 = Activity(name="Boredomtherapy", rating=4.5, location="San Francisco",
                    yelp="www.boredometherapysf.com", business_id="Boredom-therapy-SF")
    act3 = Activity(name="Pasta and Paint", rating=5, location="Kona",
                    yelp="www.pastaandpaintkona.com", business_id="Pasta-and-Paint-Kona")
    act4 = Activity(name="Filmsnfun", rating=4, location="Los Angeles",
                    yelp="www.filmsnfun-la.com", business_id="Films-n-fun-LA")

    rest1 = Restaurant(name="Nom nomz", rating=5, location="Kona",
                       yelp="www.nomnomzkona.com", business_id="Nom-nomz-Kona")
    rest2 = Restaurant(name="Yummy Time", rating=4.5, location="San Francisco",
                       yelp="www.yummytimesf.com", business_id="Yummy-Time-SF")
    rest3 = Restaurant(name="Good Stuff", rating=4, location="Los Angeles",
                       yelp="www.goodstufffoodla.com", business_id="Good-Stuff-LA")
    rest4 = Restaurant(name="Eat This", rating=4.5, location="Seattle",
                       yelp="www.eatthisseattle.com", business_id="Eat-This-Seattle")

    act_rec1 = ActivityRec(trip_id=1, activity_id=2, rec_value=3)
    act_rec2 = ActivityRec(trip_id=2, activity_id=1, rec_value=2)
    act_rec3 = ActivityRec(trip_id=4, activity_id=3, rec_value=1)

    rest_rec1 = RestaurantRec(trip_id=2, restaurant_id=4, rec_value=3)
    rest_rec2 = RestaurantRec(trip_id=3, restaurant_id=3, rec_value=2)
    rest_rec3 = RestaurantRec(trip_id=4, restaurant_id=1, rec_value=1)

    db.session.add_all([user1, user2, user3, trip1, trip2, trip3, trip4, act1,
                        act2, act3, act4, rest1, rest2, rest3, rest4, act_rec1,
                        act_rec2, act_rec3, rest_rec1, rest_rec2, rest_rec3])
    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
