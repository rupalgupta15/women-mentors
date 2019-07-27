from unittest import TestCase, main
import requests
from flask_login import current_user
from flaskmentor import forms, clean_user_input, match_mentors, app, db, bcrypt
import os
from wtforms_test import FormTestCase
from flaskmentor.models import U1, T1
# import flaskmentor


# UNCOMMENT EVERYTHING THAT SAYS "WORKING CHECKED"


# Creating a set of Database tests - to check if login and signup works fine at the database


# WORKING CHECKED:
# class DBTests(TestCase):
#     #### setup and teardown ####
#     # executed prior to each test
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/loldb'
#         self.app = app.test_client()
#         db.create_all()
#         self.assertEqual(app.debug, False)
#
#     # executed after each test
#     def tearDown(self):
#         # db.session.remove()
#         # db.drop_all()
#         pass
#
#     # Testing login for a user where username and password are saved in DB
#     def test_authentic_login(self):
#         # Test User's correct password and email
#         username = 'testuser'
#         email = "testuser@test.test"
#         password = 'test1'
#
#         user = User6.query.filter_by(email=email).first()
#         response = self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)
#         if user:
#             assert b' Login Successful!' in response.data
#             self.assertEqual(response.status_code, 200)
#
#         # Verifying same username also exists in the database
#         if user and bcrypt.check_password_hash(user.password, password):
#             self.assertEqual(user.username, username)
#
#     # Testing login for a user where username and password do not exist in DB - also verifying frontend generates error
#     # by flash messages
#
#     def test_unauthentic_login(self):
#         # User does not exist in the database
#         email = "user@test.test"
#         password = 'test1'
#
#         user = User6.query.filter_by(email=email).first()
#         response = self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)
#         if not user:
#             self.assertEqual(response.status_code, 200)
#         else:
#             assert b' Login Successful!' in response.data


# TODO: Add test for sign up as well