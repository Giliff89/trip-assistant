from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()


class User(db.Model):
    """User of Trip Assistant website."""

    __tablename__ = "users"

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=True)
    password = db.Column(db.String(64), nullable=False)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_trips'
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
