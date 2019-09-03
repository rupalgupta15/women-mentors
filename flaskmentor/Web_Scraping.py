from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import bs4
import urllib.request, re
from flaskmentor import face_detect, fetch_twitter_img_url
import json
import time
import tweepy


def getLinks(url):
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    profile_link = []
    screen_name = []
    replies = []
    replies_href = []

    for i, t in enumerate(soup.select('tr')):
        if i == 0:
            continue
        # the very first row is just the headers for table
        twitter_profile = t.findAll('td')[0].contents  # first column
        reply_to_tweet = t.findAll('td')[2].contents  # third column
        # print('twitter_profile', reply_to_tweet[1])
        if isinstance(twitter_profile[0], bs4.element.NavigableString):
            continue
        if isinstance(reply_to_tweet[1], bs4.element.NavigableString):
            continue
        url = twitter_profile[0].get('href')  # [0] here needs to be changed
        profile_link.append(url)
        s_name = url.rsplit('/', 1)[-1]
        screen_name.append(s_name)
        replies.append(reply_to_tweet[0])
        reply_url = reply_to_tweet[1].get('href')
        replies_href.append(reply_url)
        # print(first_column[0].get('href'), third_column)

    # actual_screen_name = screen_name[4:]
    actual_screen_name = screen_name
    return actual_screen_name, replies, replies_href


    # 2nd way to fetch the link from the first column
    # links = []
    # screen_name = []
    #
    # for link in soup.findAll('a', href=re.compile('https://twitter\.com/')):
    #     # / fall - open - house\?.*
    #     print('link', link)
    #     url = link.get('href')
    #     links.append(url)
    #     print('links', links)
    #     s_name = url.rsplit('/', 1)[-1]
    #     screen_name.append(s_name)
    #
    # actual_data = screen_name[4:]
    # return actual_data


# To add the users to json format:
# consumer_key = os.getenv("CONSUMER_KEY_TWITTER")
# consumer_secret = os.getenv("CONSUMER_SECRET_TWITTER")
# access_token = os.getenv("ACCESS_KEY_TWITTER")
# access_token_secret = os.getenv("ACCESS_SECRET_TWITTER")

consumer_key = "" # TODO: Add consumer key
consumer_secret = "" # TODO: Add consumer secret
access_token = "" # TODO: Add access token
access_token_secret = "" # TODO: Add access token secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def fetch_all_mentors():
    # users_dict = {"mentors": []}   # used before - working correctly
    users_dict = {}
    # for q in query_list:
    screen_names, replies, replies_link = getLinks("https://ishansharma.github.io/twitter-mentors/")
    for i, name in enumerate(screen_names):
        # calling sleep to avoid face API rate limit error
        time.sleep(4)
        # API.search_users(q[, per_page][, page])
        # per_page - max 20 number of statuses to receive,
        # page - page number of results to receive
        # users_dict["mentors"].append(user._json)  # used before - working correctly
        # Below two lines added new - not working
        try:
            user = api.get_user(screen_name=name)
            temp_dict = user._json
            # the following columns also need to be added in the other file from which you are getting other mentors

            # only mentors from this file will have additional replies, so we can set the flag to Y here but N elsewhere
            temp_dict['replies_flag'] = 'Y'
            temp_dict['additonal_replies'] = replies[i]
            temp_dict['additonal_replies_link'] = replies_link[i]

            # processing for gender:
            original_profile_pic = fetch_twitter_img_url.return_original_profile_pic(temp_dict['profile_image_url_https'])
            # print('original_profile_pic', original_profile_pic)
            temp_dict['gender_val'] = face_detect.get_gender_details(original_profile_pic)

            # print('modified temp_dict', temp_dict)
            users_dict[temp_dict['id_str']] = temp_dict
        except tweepy.error.TweepError:
            continue

    with open('../data/test_replies_mentor_data.json', 'w') as f:
        json.dump(users_dict, f, indent=4)


fetch_all_mentors()
