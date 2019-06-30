import json

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

from textblob import TextBlob
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

consumer_key = "9jurSy2yLbPaGLPr3mBnoq61b"
consumer_secret = "8Ymv6VJAGvOAXD5F8upt3iLbdsFBkj3rauToRKgFXJrOdx5jpn"
access_token = "526834125-KNkrRzAiYGv7dcBnbg78VQ3eYWueGaxeXMwTOuXW"
access_token_secret ="ZdELv0MenDKsTXoef5sqyxd0MtZwtkCadVo9t9vUXOoZ1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def find_all_users(q, num_of_mentors=100):
    num_results_per_page = 20
    num_pages = math.ceil(num_of_mentors/num_results_per_page)

    # users_dict = {"mentors": []}   # used before - working correctly
    users_dict = {}
    # for q in query_list:
    for i in range(1, num_pages+1):
        for user in api.search_users(q, num_results_per_page, i):
            # API.search_users(q[, per_page][, page])
            # per_page - max 20 number of statuses to receive,
            # page - page number of results to receive
            # users_dict["mentors"].append(user._json)  # used before - working correctly
            # Below two lines added new - not working
            temp_dict = user._json
            users_dict[temp_dict['id_str']] = temp_dict

    with open('./data/programming_mentor_data.json', 'w') as f:
        json.dump(users_dict, f, indent=4)


find_all_users('programming mentor', 100)



# print(users)
# # print(api.verify_credentials())
# print(api.search_users('women mentor', 20, 5))