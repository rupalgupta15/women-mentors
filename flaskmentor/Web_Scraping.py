from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request, re

import json
import tweepy
import math


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def getLinks(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')

    # for i, t in enumerate(soup.select('tr')):
    #     print(i, t.text)

    links = []
    screen_name = []

    for link in soup.findAll('a', href=re.compile('https://twitter\.com/')):
        # / fall - open - house\?.*
        url = link.get('href')
        links.append(url)
        s_name = url.rsplit('/', 1)[-1]
        screen_name.append(s_name)

    actual_data = screen_name[4:]
    return actual_data


# Example:
# NOT IN USE:
# raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
# html = BeautifulSoup(raw_html, 'html.parser')
# for i, li in enumerate(html.select('li')):
#     print(i, li.text)
# Actual:
# raw_html = simple_get('http://stephaniehurlburt.com/blog/2016/11/14/list-of-engineers-willing-to-mentor-you')
# print(len(raw_html))  # 95023
# raw_html = simple_get('http://stephaniehurlburt.com/blog/2016/11/14/list-of-engineers-willing-to-mentor-you')
# html = BeautifulSoup(raw_html, 'html.parser')
# for i, p in enumerate(html.select('p')):
#     print(i, p.text)
# for i, p in enumerate(html.select('blockquote')):
#     print(i, p.text)
# NOT IN USE TILL HERE


# FINAL IN USE: An even better site to scrape the data is : https://ishansharma.github.io/twitter-mentors/
# raw_html = simple_get('https://ishansharma.github.io/twitter-mentors/')
# html = BeautifulSoup(raw_html, 'html.parser')
# for i, t in enumerate(html.select('tr')):
#     print(i, t.text)
    # print(getLinks("https://ishansharma.github.io/twitter-mentors/") )

# for i, p in enumerate(html.select('blockquote')):
#     print(i, p.text)

# print( getLinks("https://ishansharma.github.io/twitter-mentors/") )


# To add the users to json format:

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

def fetch_all_mentors():
    # users_dict = {"mentors": []}   # used before - working correctly
    users_dict = {}
    # for q in query_list:
    screen_names = getLinks("https://ishansharma.github.io/twitter-mentors/")
    for name in screen_names:
        # API.search_users(q[, per_page][, page])
        # per_page - max 20 number of statuses to receive,
        # page - page number of results to receive
        # users_dict["mentors"].append(user._json)  # used before - working correctly
        # Below two lines added new - not working
        try:
            user = api.get_user(screen_name=name)
            temp_dict = user._json
            users_dict[temp_dict['id_str']] = temp_dict
        except tweepy.error.TweepError:
            continue

    with open('../data/replies_mentor_data.json', 'w') as f:
        json.dump(users_dict, f, indent=4)


fetch_all_mentors()