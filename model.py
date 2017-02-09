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
    term_1 = db.Column(db.String(30), nullable=True)
    term_2 = db.Column(db.String(30), nullable=True)
    term_3 = db.Column(db.String(30), nullable=True)
    term_4 = db.Column(db.String(30), nullable=True)
    term_5 = db.Column(db.String(30), nullable=True)


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
    # location as a city (zipcode) for Yelp search capability
    # One trip maps to one user, but a user can have many trips in their profile.

    users = db.relationship('User')


class Recommendation(db.Model):
    """One day of recommendations for a trip."""

    __tablename__ = "recommendations"

    rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'),
                              nullable=False)
    activity_id = db.Column(db.Integer,
                            db.ForeignKey('activities.activity_id'),
                            nullable=False)
    day_num = db.Column(db.Integer, nullable=True)


class Activity(db.Model):
    """Single activity recommendation."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    yelp_business_id = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(256), nullable=False)
    # may want to add key terms section


class Restaurant(db.Model):
    """Single restaurant recommendation."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    yelp_business_id = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(256), nullable=False)
    # may want to add key terms section


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recommendations'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


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


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
