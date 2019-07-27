from flaskmentor import db, login_manager, app  # db should be present in init.py
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.collections import attribute_mapped_collection


# Takes user id as argument
# decorate the function
@login_manager.user_loader
def load_user(user_id):
    return User6.query.get(int(user_id))


# Class for users
class User6(db.Model, UserMixin):
    # columns
    # __tablename__ = "users"  # to get old users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)
    # After adding twitter Oauth making password and email nullable = True
    # hashing algorithm will make this string as 60 char long
    # description = db.Column(db.String(250))
    owner = db.relationship('Test6', backref='owner', lazy=True)
    # backref is similar to adding another column to Details model - details will be added as description

    # Magic Method: How object is printed when we print it (also __scr__)
    def __repr__(self):
        return f"User6('{self.id}, {self.username}, {self.email}, {self.owner}')"


class Test6(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mentorskills = db.Column(db.String(200), nullable=False)
    location = db.Column(db.Text, nullable=True)
    preference = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user6.id'), nullable=False)

    # Id of user
    # In user model, Posts is started with capital letter because we are using the actual Post class.
    # But here we use 'user.id' with small u because it is actual table in db, and actual column
    # table and column name are simply lowercase by default

    def __repr__(self):
        return f"Test6('{self.id}, {self.mentorskills}, {self.location}, {self.preference}, {self.user_id}')"


# https://github.com/singingwolfboy/flask-dance-multi-provider/blob/master/app/models.py
class OAuth(OAuthConsumerMixin, db.Model):
    # __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
    provider_user_id = db.Column(db.String(256), nullable=False, unique=True)
    # provider_user_login = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User6.id), nullable=False)
    user = db.relationship(
        User6
        # This `backref` thing sets up an `oauth` property on the User model,
        # which is a dictionary of OAuth models associated with that user,
        # where the dictionary key is the OAuth provider name.
        # backref=db.backref(
        #     "oauth",
        #     collection_class=attribute_mapped_collection("provider"),
        #     cascade="all, delete-orphan",
        # ),
    )


# Steps to be able to make entry to database:
# python
# from flaskmentor import db
# db.create_all()
# from flaskmentor.models import User, Details
# User6.query.all()
# Test6.query.join(U1).filter(U1.id==1).all()
# On heroku:
# heroku run python
# from flaskmentor import db
# db.create_all()



#  Current database in Heroku is by the names of User6 and Test6.
#  26 July database in Heroku is by the names of U1 and T1.
# Heroku only works with User6 and Test6 databases, failed miserably when U1 and T1 used.
# But now database has issue in heroku - sign up does not work at all



# POSTGRESQL, commands:
# /Applications/Postgres.app/Contents/Versions/11/bin/psql -p5432 "postgres"  - to enter into postgre sql
# \list - to list all databases on the server
# \c test - to connect to the test database
# \dt - to see all the tables created so far
#

# For testing I used the same test db named as unittest - https://stackoverflow.com/a/876565/7862857
# using commands:
# CREATE DATABASE newdb WITH TEMPLATE test;
# SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'test' AND pid <> pg_backend_pid();                                                                                                                       WHERE pg_stat_activity.datname = 'test' AND pid <> pg_backend_pid();


