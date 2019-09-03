import json
from flaskmentor import face_detect, fetch_twitter_img_url
import tweepy

import pandas as pd
import numpy as np
import os
import time
import math

import sqlite3

# consumer_key = os.getenv("CONSUMER_KEY_TWITTER")
# consumer_secret = os.getenv("CONSUMER_SECRET_TWITTER")
# access_token = os.getenv("ACCESS_KEY_TWITTER")
# access_token_secret = os.getenv("ACCESS_SECRET_TWITTER")

consumer_key = ""  # TODO: Add consumer key
consumer_secret = ""  # TODO: Add consumer secret
access_token = ""  # TODO: Add access token
access_token_secret = ""  # TODO: Add Access token secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
# print(api.get_user(screen_name='yoyuull'))


def find_all_users(q, filename, num_of_mentors=100):
    num_results_per_page = 20  # This is the limit
    num_pages = math.ceil(num_of_mentors/num_results_per_page)

    # users_dict = {"mentors": []}   # used before - working correctly
    users_dict = {}
    # for q in query_list:
    for i in range(1, num_pages+1):
        for user in api.search_users(q, num_results_per_page, i):
            time.sleep(4)
            # API.search_users(q[, per_page][, page])
            # per_page - max 20 number of statuses to receive,
            # page - page number of results to receive
            # users_dict["mentors"].append(user._json)  # used before - working correctly
            # Below two lines added new - not working
            temp_dict = user._json
            temp_dict['replies_flag'] = 'N'
            # temp_dict['extra_details'] = ""
            # processing for gender:
            # if gender already available for this mentor, do not call MSFT API
            original_profile_pic = fetch_twitter_img_url.return_original_profile_pic(temp_dict['profile_image_url_https'])
            temp_dict['gender_val'] = face_detect.get_gender_details(original_profile_pic)

            users_dict[temp_dict['id_str']] = temp_dict

    # with open('../data/aerospace_mentor_data.json', 'w') as f:
    with open('../data/'+ filename, 'w') as f:
        json.dump(users_dict, f, indent=4)


# find_all_users('astronomy mentor', 'astronomy_mentor_data.json', 300)
# find_all_users('biochemistry mentor', 'biochemistry_mentor_data.json', 300)
# find_all_users('biology mentor', 'biology_mentor_data.json', 300)
# find_all_users('chemical engineering mentor', 'chemical_mentor_data.json', 300)
# find_all_users('chemistry mentor', 'chemistry_mentor_data.json', 300)
# find_all_users('civil engineering mentor', 'civil_mentor_data.json', 300)
# find_all_users('computer science mentor', 'computer_mentor_data.json', 800)
# find_all_users('engineering mentor', 'engineering_mentor_data.json', 800)

# find_all_users('electrical engineering mentor', 'electrical_mentor_data.json', 400)
# find_all_users('math mentor', 'math_mentor_data.json', 400)
# find_all_users('mathematics mentor', 'mathematics_mentor_data.json', 400)
# find_all_users('physics mentor', 'physics_mentor_data.json', 400)
# find_all_users('mechanical engineering mentor', 'mech_mentor_data.json', 400)
# find_all_users('psychology mentor', 'psychology_mentor_data.json', 400)
# find_all_users('statistics mentor', 'statistics_mentor_data.json', 400)

# find_all_users('python mentor', 'python_mentor_data.json', 400)
# find_all_users('java mentor', 'java_mentor_data.json', 400)
# find_all_users('javascript mentor', 'javascript_mentor_data.json', 400)
# find_all_users('frontend mentor', 'frontend_mentor_data.json', 400)
# find_all_users('STEM mentor', 'STEM_mentor_data.json', 400)
# find_all_users('backend mentor', 'backend_mentor_data.json', 400)
# find_all_users('programming  mentor', 'programming_mentor_data.json', 400)
# find_all_users('UI UX design mentor', 'UIUX_mentor_data.json', 400)
# find_all_users('leadership mentor', 'leader_mentor_data.json', 400)
# find_all_users('Artificial Intelligence design mentor', 'AI_mentor_data.json', 400)
# find_all_users('Machine learning mentor', 'ML_mentor_data.json', 400)
# find_all_users('social science mentor', 'social_mentor_data.json', 400)
#
# find_all_users('data science mentor', 'data_science_mentor_data.json', 200)
# find_all_users('react mentor', 'react_mentor_data.json', 200)
# find_all_users('angular mentor', 'angular_mentor_data.json', 200)
# find_all_users('vue mentor', 'vue_mentor_data.json', 200)
# find_all_users('database mentor', 'database_mentor_data.json', 200)
# find_all_users('nlp mentor', 'nlp_mentor_data.json', 200)
# find_all_users('deep learning mentor', 'deep_mentor_data.json', 200)
# find_all_users('economics mentor', 'economic_mentor_data.json', 200)
# find_all_users('geography mentor', 'geography_mentor_data.json', 200)
# find_all_users('technology mentor', 'technology_mentor_data.json', 200)
# find_all_users('women in tech mentor', 'women_tech_mentor_data.json', 200)
# find_all_users('women in STEM mentor', 'women_STEM_mentor_data.json', 200)
# find_all_users('women in tech advisor', 'women_tech_advisor_data.json', 200)
# find_all_users('women in STEM advisor', 'women_STEM_advisor_data.json', 200)
