from flaskmentor import db, login_manager, app  # db should be present in init.py
from flask_login import UserMixin


# Takes user id as argument
# decorate the function
@login_manager.user_loader
def load_user(user_id):
    return User5.query.get(int(user_id))


# Class for users
class User5(db.Model, UserMixin):
    # columns
    # __tablename__ = "users"  # to get old users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # hashing algorithm will make this string as 60 char long
    # description = db.Column(db.String(250))
    owner = db.relationship('Test5', backref='owner', lazy=True)
    # backref is similar to adding another column to Details model - details will be added as description

    # Magic Method: How object is printed when we print it (also __scr__)
    def __repr__(self):
        return f"User5('{self.id}, {self.username}, {self.email}, {self.owner}')"


class Test5(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mentorskills = db.Column(db.String(200), nullable=False)
    location = db.Column(db.Text, nullable=False)
    preference = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user5.id'), nullable=False)

    # Id of user
    # In user model, Posts is started with capital letter because we are using the actual Post class.
    # But here we use 'user.id' with small u because it is actual table in db, and actual column
    # table and column name are simply lowercase by default

    def __repr__(self):
        return f"Test5('{self.id}, {self.mentorskills}, {self.location}, {self.preference}, {self.user_id}')"

# Steps to be able to make entry to database:
# python
# from flaskmentor import db
# db.create_all()
# from flaskmentor.models import User, Details
# User.query.all()
# Test5.query.join(User5).filter(User5.id==1).all()


#  Current database in Heroku is by the names of User5 and Test5.
