from unittest import TestCase, main
import requests
from flask_login import current_user
from flaskmentor import forms, clean_user_input, match_mentors, app, db, bcrypt
import os
from wtforms_test import FormTestCase
from flaskmentor.models import U1, T1
# import flaskmentor

# mentors_test = {
#     "1": {"description": "python; mentor", "gender_val": "female"},
#     "2": {"description": "developer polyglot @software ", "gender_val": "male"},
#     "3": {"description": "polyglot", "gender_val": "female"}
# }

# UNCOMMENT EVERYTHING THAT SAYS "WORKING CHECKED"

"""
Sources: 
https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
"""


#  Third Attempt to test flask form
#
# class TestUserForm(FormTestCase):
#     form_class = forms.SignUpForm
#
#     def test_age_is_required(self):
#         self.assert_required('email')



#  Second Attempt

# class BasicTests(TestCase):
#
#     ############################
#     #### setup and teardown ####
#     ############################
#
#     # executed prior to each test
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(TEST_DB)
#         self.app = app.test_client()
#         # db.drop_all()
#         db.create_all()
#
#         self.assertEqual(app.debug, False)
#
#     # executed after each test
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         # pass
#
#     #### tests ####
#
#     # WORKING CHECKED:
#     # def test_main_page(self):
#     #     response = self.app.get('/', follow_redirects=True)
#     #     self.assertEqual(response.status_code, 200)
#
#     ########################
#     #### helper methods ####
#     ########################
#
#     def signup(self, username, email, password, confirm):
#         return self.app.post(
#             '/signup',
#             data=dict(username=username, email=email, password=password, confirm=confirm),
#             follow_redirects=True
#         )
#
#     # def login(self, email, password):
#     #     return self.app.post(
#     #         '/login',
#     #         data=dict(email=email, password=password),
#     #         follow_redirects=True
#     #     )
#     #
#     # def logout(self):
#     #     return self.app.get(
#     #         '/logout',
#     #         follow_redirects=True
#     #     )
#
#     # def test_valid_user_registration(self):
#     #     response = self.signup('TestUser1','testuser1@gmail.com', 'testpassword', 'testpassword')
#     #     self.assertEqual(response.status_code, 200)
#         # print(response)
#         # self.assertIn(b'Thanks for registering!', response.data)
#
#     def test_invalid_user_registration_different_passwords(self):
#         form_class = forms.SignUpForm
#
#         form_class.password.data = 'testpassword'
#         form_class.confirm_password.data = 'Password'
#
#         response = self.signup('TestUser1','testuser1@gmail.com', 'testpassword', 'Password')
#
#         print('emaail', form_class.email.data)
#
#         print('response', response)
#         self.assertEqual(response.status_code, 100)
#         # self.assertIn(b'Field must be equal to', response.data)
#
#
# if __name__ == "__main__":
#     main()




#  First Attempt
# class TestUserForms(TestCase):
#
#     # # TODO: TEST FAILS
#     # def test_login(self):
#     #     # Ensure incorrect data does not validate.
#     #     form = forms.LoginForm(email='newuser@test.test',
#     #         password='newuser123', confirm='')
#     #     self.assertFalse(form.validate())
#     #     self.assertEqual(1, 1)
#
#     # WORKING CHECKED: TEST RUNS FOR RECOMMENDATION BACKEND
#     def test_recommendation(self):
#         q = "polyglot software developer"
#         q_list = clean_user_input.main(q)
#         results = match_mentors.main(q_list, "unittest.json")
#         print(results)
#         self.assertEqual(len(results), 2)
#         self.assertEqual(results[0]['id'], 2240)
#         self.assertEqual(results[1]['id'], 15667722)
#
#         # testing empty query
#         q = ""
#         q_list = clean_user_input.main(q)
#         results = match_mentors.main(q_list, "unittest.json")
#         self.assertEqual(len(results), 3)
#
#
#         # non matched stuff
#         q = "java"
#         q_list = clean_user_input.main(q)
#         results = match_mentors.main(q_list, "unittest.json")
#         self.assertEqual(len(results), 0)
#
#         # code with unwanted characters
#         q = "polyglot$software,.*developer"
#         q_list = clean_user_input.main(q)
#         print('q_list', q_list)
#         results = match_mentors.main(q_list, "unittest.json")
#         print(results)
#         self.assertEqual(len(results), 2)
#         self.assertEqual(results[0]['id'], 2240)
#         self.assertEqual(results[1]['id'], 15667722)
#
#
#     # TODO: LEFT - TESTING THE SEARCH FUNTIONALITY
#     def test_search(self):
#         r = requests.get('https://www.womenmentors.co/search?query=new%20york')
#         print('r', r.text)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         self.assertEqual(1,2)


# class TestUserViews(TestCase):
#
#     def test_login(self):


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


# TODO: Add test for sign up as well in the DBtest class