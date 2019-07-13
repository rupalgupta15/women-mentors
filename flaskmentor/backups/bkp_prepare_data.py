from pandas import DataFrame
import pandas as pd
import json
from nltk import word_tokenize
from collections import defaultdict
import re
regex = re.compile("[^a-zA-Z0-9 ]") #100ms


def tokenize(sentence):
    nltk_tokens = word_tokenize(sentence)
    return nltk_tokens


def matches(mentor_des, user_query): # mentor_des is a list
    intersection = len(list(set(user_query).intersection(mentor_des)))
    return intersection


def main(user_query):
    # Fetching data from mentors json file to a dictionary
    final_matched_mentors = []
    mentors_dict = {}

    with open('./data/final_mentors.json', 'r') as f:
        # temp_data = json.load(f)
        final_data = json.load(f)
    # final_data = temp_data["mentors"]

    for user in final_data:
        temp_dict = user
        mentors_dict[temp_dict['id_str']] = temp_dict

    # print(mentors_dict.keys()

    for key, value in mentors_dict.items():
        mentors_dict[key]['clean_description'] = regex.sub("", mentors_dict[key]['description'])
        mentors_dict[key]['clean_description'] = mentors_dict[key]['clean_description'].lower()

    # print(mentors_dict['2689638530']['clean_description'])

    for key, value in mentors_dict.items():
        mentors_dict[key]['tokenized_description'] = tokenize(mentors_dict[key]['clean_description'])


    match_counts_dict = defaultdict(list)
    for key, value in mentors_dict.items():
        match_counts_dict[matches(mentors_dict[key]['tokenized_description'], user_query)].append(mentors_dict[key]['id_str'])

    # print(match_counts_dict)
    max_key_val = max(match_counts_dict.keys())
    # print(max_key_val)
    # print(match_counts_dict[max_key_val])
    matched_ids = match_counts_dict[max_key_val]

    for id in matched_ids:
        # print(mentors_dict[id])
        individuals = mentors_dict[id]
        fetch_mentor = {"id": individuals["id"], "name": individuals["name"],  "location": individuals["location"],
                        "description": individuals["description"], "other_urls": individuals["url"],
                        "followers_count": individuals["followers_count"], "friends_count": individuals["friends_count"],
                        "profile_pic_url": individuals["profile_image_url_https"],
                        }

        final_matched_mentors.append(fetch_mentor)

    # print(final_matched_mentors)
    # Create final object to be returned
    return final_matched_mentors

# main('women')