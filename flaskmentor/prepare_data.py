import json
from nltk import word_tokenize
from collections import defaultdict
import os
import re

regex = re.compile("[^a-zA-Z0-9 ]")  # 100ms


def tokenize(sentence):
    nltk_tokens = word_tokenize(sentence)
    return nltk_tokens


def preprocess(string):
    """ Remove punctuations from a string, remove excess whitespace
    Returns: clean string
    """
    cleaned = regex.sub("", string)
    return cleaned.lower()


def matches(mentor_des, user_query):  # mentor_des and user_query both are lists
    # Make sure the two types are usually the same
    intersection = len(list(set(mentor_des).intersection(user_query)))
    return intersection


def user_query_processing(user_query, mentors_dict):
    user_query = preprocess(user_query)
    user_query_list = tokenize(user_query)
    match_counts_dict = defaultdict(list)

    for key, value in mentors_dict.items():
        key_dict = matches(mentors_dict[key]['tokenized_description'], user_query_list)
        match_counts_dict[key_dict].append(mentors_dict[key]['id_str'])

    sorted_match_count_dict = list(sorted(match_counts_dict.keys()))
    max_key_val = sorted_match_count_dict[-1]   # max(match_counts_dict.keys())
    matched_ids = match_counts_dict[max_key_val]
    if len(matched_ids) == 0:
        print("Sorry, no matches found")
    elif len(matched_ids) > 5:
        matched_ids = matched_ids
    else:
        for i in range(0, 5-len(matched_ids)):  # return items from second highest key in dict
            sec_max_key_id = sorted_match_count_dict[-2]
            matched_ids = match_counts_dict[sec_max_key_id]
    return matched_ids


# 2 main files: final_mentors.json (this contains self selected data from twitter) and replies_mentor_data.json
# (this file has all the data fetched from replies) (pass user query None for accessing this file's contents)
def main(user_query="", filename="final_mentors.json"):
    # Fetching data from mentors json file to a dictionary
    final_matched_mentors = []
    # mentors_dict = {}

    path = './data/' + filename

    with open(path, 'r') as f:
        # temp_data = json.load(f)
        mentors_dict = json.load(f)
    # final_data = temp_data["mentors"]

    # for user in final_data:
    #     temp_dict = user
    #     mentors_dict[temp_dict['id_str']] = temp_dict

    for key, value in mentors_dict.items():
        mentors_dict[key]['clean_description'] = preprocess(mentors_dict[key]['description'])
        # mentors_dict[key]['clean_description'] = mentors_dict[key]['clean_description'].lower()

    for key, value in mentors_dict.items():
        mentors_dict[key]['tokenized_description'] = tokenize(mentors_dict[key]['clean_description'])

    if user_query:
        filtered_ids = user_query_processing(user_query, mentors_dict)
    else:
        filtered_ids = []
        for key, value in mentors_dict.items():
            filtered_ids.append(mentors_dict[key]['id_str'])

    for id in filtered_ids:
        individuals = mentors_dict[id]
        # Include mentors whose profile is not protected - this is because we want them to find mentors easily
        if not individuals["protected"]:
            # print('individuals["protected"]', individuals["protected"])

            f_name, f_ext = os.path.splitext(individuals["profile_image_url_https"])
            f_name = f_name.replace("_normal", "")
            original_profile_pic = f_name + f_ext

            # print('original_profile_pic', original_profile_pic)

            fetch_mentor = {"id": individuals["id"], "name": individuals["name"], "location": individuals["location"],
                            "description": individuals["description"], "other_urls": individuals["url"],
                            "followers_count": individuals["followers_count"], "friends_count": individuals["friends_count"],
                            "profile_pic_url": original_profile_pic,
                            "twitter_profile_url": "https://twitter.com/"+individuals["screen_name"]
                            }
        else:
            continue
        final_matched_mentors.append(fetch_mentor)
    # Create final object to be returned

    return final_matched_mentors  # This should be the object created above which is a list of dictionaries


# For directly testing this file change ./data to ../data
# final_matched_mentors = main(None, filename="replies_mentor_data.json")
# print('final_matched_mentors', final_matched_mentors)