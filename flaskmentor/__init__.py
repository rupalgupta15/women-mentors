# This is a package to initialize application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_heroku import Heroku
import logging
from flask import Flask
import sys


app = Flask(__name__)
app.app_context().push()  # Added only for unit test

# next 2 lines added for logging error to heroku logs
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = '17b60f8a1367103ecd4d09eda9426caf'
# can be made an environment variable : To be only used locally, for heroku use next command
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test'

# For heroku:
heroku = Heroku(app)

# three slashes are relative path from current file
db = SQLAlchemy(app)  # instance of SQLAlchemy db
# # class is a table in database, database structures can be represented as class called modules
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# # login route is set here
login_manager.login_message_category = 'info'

# Watch out for circular imports
from flaskmentor import routes