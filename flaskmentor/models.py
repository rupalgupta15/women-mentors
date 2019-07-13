from flaskmentor import db, login_manager, app  # db should be present in init.py
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Takes user id as argument
# decorate the function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Class for users
class User(db.Model, UserMixin):
    # columns
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # hashing algorithm will make this string as 60 char long
    description = db.Column(db.String(250))

    # Magic Method: How object is printed when we print it (also __scr__)
    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.description}')"


# Steps to be able to make entry to database:
# python
# from flaskmentor import db
# db.create_all()
# from flaskmentor.models import User
# User.query.all()
