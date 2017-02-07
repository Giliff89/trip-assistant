from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of Trip Assistant website."""

    __tablename__ = "users"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    q1_term = db.Column(db.String(20), nullable=True)
    q2_term = db.Column(db.String(20), nullable=True)
    q3_term = db.Column(db.String(20), nullable=True)
    q4_term = db.Column(db.String(20), nullable=True)
    q5_term = db.Column(db.String(20), nullable=True)


class Trip(db.Model):
    """Trip information which maps to user_id."""

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(128), nullable=False)


class Recommendation(db.Model):
    """One day worth of recommendations for a trip."""

    rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    restaurant_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    activity_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    day_num = db.Column(db.Integer, nullable=True)


class Activity(db.Model):
    """Single activity recommendation."""

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # Can I use a Yelp id here?
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(256), nullable=False)


class Restaurant(db.Model):
    """Single restaurant recommendation."""

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # Can I use a Yelp id here?
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    yelp = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(256), nullable=False)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///trip_assistant'
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
