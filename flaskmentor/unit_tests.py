from unittest import TestCase, main
import requests
from flask_login import current_user
from flaskmentor import forms, clean_user_input, match_mentors, app, db, bcrypt
import os
from wtforms_test import FormTestCase
from flaskmentor.models import User6, Test6


# mentors_test = {
#     "1": {"description": "python; mentor", "gender_val": "female"},
#     "2": {"description": "developer polyglot @software ", "gender_val": "male"},
#     "3": {"description": "polyglot", "gender_val": "female"}
# }


class TestRecommendationAlgorithm(TestCase):
    """
    Sources and Credits:
    https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
    This test tests the working of recommendation algorithm by using a dummy file unittest.json and checking for
    different query strings being passed to this file and asserting for the expected output.
    """
    def test_recommendation(self):
        """
        To test how the algorithm works when the query match is found
        :return: True/False
        """
        q = "polyglot software developer"
        q_list = clean_user_input.main(q)
        results = match_mentors.main(skills_query=q_list, filename="unittest.json")
        print(results)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 2240)
        self.assertEqual(results[1]['id'], 15667722)

    def test_if_query_empty(self):
        """
        To test how the algorithm works when the empty query is passed
        :return: True/False
        """
        q = ""
        q_list = clean_user_input.main(q)
        results = match_mentors.main(skills_query=q_list, filename="unittest.json")
        self.assertEqual(len(results), 3)


    def test_if_query_not_present_in_file(self):
        """
        To test how the algorithm works when the query is not found in the file
        :return: True/False
        """
        q = "java"
        q_list = clean_user_input.main(q)
        results = match_mentors.main(skills_query=q_list, filename="unittest.json")
        self.assertEqual(len(results), 0)

    def test_wild_characters(self):
        """
        To test how the algorithm works when the query has various wild characters
        :return: True/False
        """
        q = "polyglot$software,.*developer"
        q_list = clean_user_input.main(q)
        print('q_list', q_list)
        results = match_mentors.main(skills_query=q_list, filename="unittest.json")
        print(results)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], 2240)
        self.assertEqual(results[1]['id'], 15667722)



# Creating a set of Database tests - to check if login and signup works fine at the database
class DBTests(TestCase):
    """
    This test tests the backend functionality of sign up, login and form validations.
    """
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/loldb'
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        pass

    def test_main_page(self):
        """
        Testing that the home page gets loaded without errors
        :return: True/False
        """
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_authorized_login(self):
        """
        Testing login for a user where username and password are saved in DB
        :return: True/False
        """
        # Test User's correct password and email
        username = 'testuser'
        email = "testuser@test.test"
        password = 'test1'

        user = User6.query.filter_by(email=email).first()
        response = self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)
        if user:
            assert b' Login Successful!' in response.data
            self.assertEqual(response.status_code, 200)

        # Verifying same username also exists in the database
        if user and bcrypt.check_password_hash(user.password, password):
            self.assertEqual(user.username, username)

    def test_unauthentic_login(self):
        """
        Testing login for a user where username and password do not exist in DB - also verifying frontend generates error by flash messages
        :return: True/False
        """
        # User does not exist in the database
        email = "user@test.test"
        password = 'test1'

        user = User6.query.filter_by(email=email).first()
        response = self.app.post('/login', data=dict(email=email, password=password), follow_redirects=True)
        if not user:
            self.assertEqual(response.status_code, 200)
        else:
            assert b' Login Successful!' in response.data

    def test_signup(self):
        """
        Testing sign up functionality - when the user signs up, database is updated successfully
        :return: True/False
        """
        # User does not exist in the database yet
        # Note that if this test fails, please try it with changing username, email, password and confirm_password
        username = 'signup1'
        email = "signupuser1@test.test"
        password = 'signup1'
        confirm_password = 'signup1'

        response = self.app.post('/signup', data=dict(username=username, email=email, password=password, confirm_password=confirm_password), follow_redirects=True)

        user = User6.query.filter_by(email=email).first()

        if not user:  # if the user is not present already, the application will not raise error
            self.assertEqual(response.status_code, 200)
        else:
            print('Assertion True')
            assert b' Your account has been created!' in response.data

    def test_duplicate_signup(self):
        """
        The app generates error if we try to login with a username that already exists
        :return: True/False
        """
        # User already exists in the database, the signup page should generate error
        username = 'signup1'
        email = "signupuser1@test.test"
        password = 'signup1'
        confirm_password = 'signup1'

        response = self.app.post('/signup', data=dict(username=username, email=email, password=password, confirm_password=confirm_password), follow_redirects=True)

        user = User6.query.filter_by(email=email).first()

        if user:  # user is already present in the database, the application will raise error, hence asserting for the error
            assert b'The username already exists. Please choose a different one.' in response.data
            assert b'The email already exists. Please choose a different one.' in response.data


    def test_incorrect_email_format(self):
        """
        Checking if the email has incorrect format
        :return: True/False
        """
        # User does not exist in the database
        username = 'signup2'
        email = "signup2.test.com"
        password = 'signup2'
        confirm_password = 'signup2'

        response = self.app.post('/signup', data=dict(username=username, email=email, password=password, confirm_password=confirm_password), follow_redirects=True)

        user = User6.query.filter_by(email=email).first()

        if not user:  # user is not present in the database, but email is incorrect hence the application will raise error. Therefore asserting for the error raised
            assert b'Invalid email address.' in response.data

    def test_password_confirm_mismatch(self):
        """
        Checking if the password and confirm password are different
        :return: True/False
        """
        # User does not exist in the database
        username = 'signup3'
        email = "signup3@test.com"
        password = 'signup3'
        confirm_password = 'signup_1'

        response = self.app.post('/signup', data=dict(username=username, email=email, password=password, confirm_password=confirm_password), follow_redirects=True)

        user = User6.query.filter_by(email=email).first()

        if not user:  # user is not present in the database, but password and confirm_password are different hence the application will raise error. Therefore asserting for the error raised
            assert b'Field must be equal to password.' in response.data

    def test_missing_username(self):
        """
        Checking if the required fields like username is not provided, if the application raises error
        :return: True/False
        """
        # User does not exist in the database
        username = ''
        email = "signup4@test.com"
        password = 'signup4'
        confirm_password = 'signup4'

        response = self.app.post('/signup', data=dict(username=username, email=email, password=password, confirm_password=confirm_password), follow_redirects=True)

        user = User6.query.filter_by(email=email).first()

        if not user:  # user is not present in the database, but password and confirm_password are different hence the application will raise error. Therefore asserting for the error raised
            assert b'This field is required.' in response.data

# To run the tests, execute:
# nosetests unit_tests.py