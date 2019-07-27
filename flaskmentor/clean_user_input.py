import json
from nltk import word_tokenize
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
    cleaned = regex.sub(" ", string)
    # cleaned = regex.sub('\s+', ' ', string).strip()
    return cleaned.lower()


def main(user_query=""):
    #  ALSO REFER TO CODE IN MATCH MENTORS.py and other places where the above two functions aare used direectly
    user_query_list = []

    if user_query:
        user_query = preprocess(user_query)
        user_query_list = tokenize(user_query)

    return user_query_list  # This should be the object created above which is a list of dictionaries

