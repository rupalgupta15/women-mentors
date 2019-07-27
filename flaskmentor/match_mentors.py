import json
from nltk import word_tokenize
from collections import defaultdict
from flaskmentor import fetch_twitter_img_url
import os, requests
from PIL import Image
import re

regex = re.compile("[^a-zA-Z0-9 ]")  # 100ms


def tokenize(sentence):
    nltk_tokens = word_tokenize(sentence)
    return nltk_tokens


def preprocess(string):
    """ Remove punctuations from a string, remove excess whitespace
    Returns: clean string
    """
    cleaned = regex.sub(" ", string)
    return cleaned.lower()


def matches(mentor_des, user_query):  # mentor_des and user_query both are lists
    # Make sure the two types are usually the same
    intersection = len(list(set(mentor_des).intersection(user_query)))
    return intersection


def loc_query_processing(loc_query_list, filtered_dict):
    match_counts_dict = defaultdict(list)
    for key, value in filtered_dict.items():
        key_dict = matches(filtered_dict[key]['tokenized_location'], loc_query_list)
        match_counts_dict[key_dict].append(filtered_dict[key]['id_str'])
    sorted_match_count_dict = list(sorted(match_counts_dict.keys(), reverse=True))
    max_key_val = sorted_match_count_dict[0]   # maximum matches
    matched_ids = []
    if max_key_val == 0:
        return matched_ids
    for key in sorted_match_count_dict:
        if key == 0 or len(matched_ids) >= 10:
            return matched_ids[:30]
        matched_ids.extend(match_counts_dict[key])
    return matched_ids[:30]


def user_query_processing(user_query_list, mentors_dict):
    match_counts_dict = defaultdict(list)
    for key, value in mentors_dict.items():
        key_dict = matches(mentors_dict[key]['tokenized_description'], user_query_list)
        match_counts_dict[key_dict].append(mentors_dict[key]['id_str'])
    sorted_match_count_dict = list(sorted(match_counts_dict.keys(), reverse=True))
    # sort list of possible matches  => sorted_match_count_dict
    # pick elements from the end of the list and corresponding dict until there are atleast 10 mentors max 30.
    max_key_val = sorted_match_count_dict[0]   # max(match_counts_dict.keys())
    # if the last element in sorted list is 0, then no results found:
    matched_ids = []
    if max_key_val == 0:
        return matched_ids
    for key in sorted_match_count_dict:
        if key == 0 or len(matched_ids) >= 10:
            print('returned on home?')
            return matched_ids[:30]
        matched_ids.extend(match_counts_dict[key])
    return matched_ids[:30]


def get_data(final_filtered_ids, mentors_dict):
    final_matched_mentors = []
    for id in final_filtered_ids:
        individuals = mentors_dict[id]
        # Include mentors whose profile is not protected - this is because we want them to connect with mentors easily
        if not individuals["protected"]:
            original_profile_pic = fetch_twitter_img_url.return_original_profile_pic(
                individuals["profile_image_url_https"])
            fetch_mentor = {"id": individuals["id"], "id_str": individuals["id_str"], "name": individuals["name"],
                            "location": individuals["location"],
                            "tokenized_location": individuals["tokenized_location"],
                            "description": individuals["description"], "other_urls": individuals["url"],
                            "followers_count": individuals["followers_count"],
                            "friends_count": individuals["friends_count"],
                            "profile_pic_url": original_profile_pic,
                            "twitter_profile_url": "https://twitter.com/" + individuals["screen_name"],
                            "gender": individuals["gender_val"], "replies_flag": individuals["replies_flag"],
                            "additonal_replies": individuals.get("additonal_replies"),
                            "additonal_replies_link": individuals.get("additonal_replies_link")
                            }
        else:
            continue
        final_matched_mentors.append(fetch_mentor)
    # Create final object to be returned
    return final_matched_mentors  # This should be the object created above which is a list of dictionaries


# NOTE: the following comment is no longer valid - as all the data is now present in final_mentors.json
# 2 main files: final_mentors.json (this contains self selected data from twitter) and test_replies_mentor_data.json
# (this file has all the data fetched from replies) (pass user query None for accessing this file's contents)
def main(skills_query=None, loc_query=None, filename="final_mentors.json"):
    # both queries will come in the form of a list - mostly containing only 1 element
    # Fetching data from mentors json file to a dictionary
    path = './data/' + filename
    # for unit test to work,  might need to change it to ../data

    with open(path, 'r') as f:
        # temp_data = json.load(f)
        mentors_dict = json.load(f)

    for key, value in mentors_dict.items():
        mentors_dict[key]['clean_description'] = preprocess(mentors_dict[key]['description'])
        mentors_dict[key]['clean_location'] = preprocess(mentors_dict[key]['location'])

    for key, value in mentors_dict.items():
        mentors_dict[key]['tokenized_description'] = tokenize(mentors_dict[key]['clean_description'])
        mentors_dict[key]['tokenized_location'] = tokenize(mentors_dict[key]['clean_location'])

    if not skills_query:
        # logic goes here for the home page
        filtered_ids = []
        for key, value in mentors_dict.items():
            filtered_ids.append(mentors_dict[key]['id_str'])
    elif len(skills_query) > 0:
        filtered_ids = user_query_processing(skills_query, mentors_dict)

    # if no location query - do nothing, the filtered id coming from above will be passed - this method is also used on
    # other pages like home page etc. If location then create a new set of ids matching and non matching and
    #  give preference to matching ids first and then non matching ids

    print('len filtered_ids', len(filtered_ids))
    if len(filtered_ids) == 0:
        if loc_query and len(loc_query) > 0:
            return [], []
        else:
            return []

    # Code for location:
    filtered_dict = {k: mentors_dict.get(k, None) for k in filtered_ids}
    if loc_query and len(loc_query) > 0:  # does not get checked if loc_query is None
        matching_loc_ids = loc_query_processing(loc_query, filtered_dict)
        print('matching_loc_ids', matching_loc_ids)
        non_matching_loc_ids = list(set(filtered_ids).difference(matching_loc_ids))
        print('len non_matching_loc_ids', len(non_matching_loc_ids))
        matched_loc_list = get_data(matching_loc_ids, mentors_dict)
        not_matched_loc_list = get_data(non_matching_loc_ids, mentors_dict)
        return matched_loc_list, not_matched_loc_list
    else:  # for the route of home, data is returned from this else
        final_matched_mentors = get_data(filtered_ids, mentors_dict)
        return final_matched_mentors
        # Code for location ends

# For directly testing this file change ./data to ../data
# final_matched_mentors = main(None, filename="test_replies_mentor_data.json")
# print('final_matched_mentors', final_matched_mentors)
