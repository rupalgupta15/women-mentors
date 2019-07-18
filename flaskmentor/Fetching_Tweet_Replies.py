# THIS FILE IS NOT IN USE

# from twitter import *
# import os
#
# # consumer_key = os.getenv("CONSUMER_KEY_TWITTER")
# # consumer_secret = os.getenv("CONSUMER_SECRET_TWITTER")
# # access_token = os.getenv("ACCESS_KEY_TWITTER")
# # access_token_secret = os.getenv("ACCESS_SECRET_TWITTER")
#
# consumer_key = "9jurSy2yLbPaGLPr3mBnoq61b"
# consumer_secret = "8Ymv6VJAGvOAXD5F8upt3iLbdsFBkj3rauToRKgFXJrOdx5jpn"
# access_token = "526834125-KNkrRzAiYGv7dcBnbg78VQ3eYWueGaxeXMwTOuXW"
# access_token_secret ="ZdELv0MenDKsTXoef5sqyxd0MtZwtkCadVo9t9vUXOoZ1"
#
# t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))  #, retry=True
#
# # reply = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=50)
# reply = t.search.tweets(q="https://twitter.com/nytimes/status/1129139682569261056", count=5)
#
# reply_tweets = {}
#
# print('result', reply)
# print('WTF', len(reply))
#
# # if reply['statuses']:  # If something is returned : this is a list of dictionaries
# #     for i in range(0, len(reply['statuses'])):
# #         # Removing replies that are retweets and less than 45 chars in length
# #         print('YOOPO', reply['statuses'][i]['text'])
# #         print('YOOPO', len(reply['statuses'][i]['text']) > 45)
# #         print('WUHUHUU', reply['statuses'][i]['user']['description'].encode('utf-8'))
# #         if (reply['statuses'][i]['text'].find('RT ') == -1) and (len(reply['statuses'][i]['text']) > 45):
# #             print('look at this', reply['statuses'][i]['user']['id'])
#             # reply_tweets[reply['statuses'][i]['id']] = {
#             #     'text': reply['statuses'][i]['text'].encode('utf-8'),
#             #     'user': {
#             #         'id': reply['statuses'][i]['user']['id'],
#             #         'name': reply['statuses'][i]['user']['name'].encode('utf-8'),
#             #         'profile': 'https://twitter.com/' + reply['statuses'][i]['user']['screen_name'].encode('utf-8'),
#             #         'description': reply['statuses'][i]['user']['description'].encode('utf-8')
#             #     }
#             # }
# #
# # print('reply_tweets', reply_tweets)



# Copied:

from twitter import *
import io, json, re

consumer_key = "9jurSy2yLbPaGLPr3mBnoq61b"
consumer_secret = "8Ymv6VJAGvOAXD5F8upt3iLbdsFBkj3rauToRKgFXJrOdx5jpn"
access_token = "526834125-KNkrRzAiYGv7dcBnbg78VQ3eYWueGaxeXMwTOuXW"
access_token_secret ="ZdELv0MenDKsTXoef5sqyxd0MtZwtkCadVo9t9vUXOoZ1"


def escape_text_for_table(text):
    # first, escape the pipe character. They conflict with table pipes on GH pages
    text = str.replace(text, '|', '\|')

    # remove new lines from the text. They cause new row to appear in GH pages table
    text = str.replace(text, '\n', ' ')

    return text


# helper function of make_twitter_link_clickable
def markdown_link(match):
    groups = match.groups() or ''
    link = groups[0]

    return '[{0}]({0})'.format(link)


# the tweets are not in search results. At the end, there is a link. Make link clickable
# so visitors can go to the specific tweet to reply or
def make_twitter_link_clickable(text):
    # The link to tweet is at end of text
    replaced = re.sub('(https\://t.co/.*)', markdown_link, text)
    return replaced


t = Twitter(
    auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

# since quotes are normal tweets with Tweet URL at end, searching API for the tweet link
result = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=100)

# result is a dictionary with 'serach_metadata' and 'statuses' keys
tweets = {}

# a bit of markdown for README page in /docs
output = "This page contains a list of people (along with their tweets) who are willing to help/mentor other programmers. I am working on a searchable index. For now, just do a Ctrl/Cmd + F and see if you can find the tech you want help with."
output += "\n\nIf you notice something wrong or want to be removed, open a GitHub issue or tweet me at [@real_ishan](https://twitter.com/real_ishan)"
output += "\n\nThanks to [Stephanie Hurlburt](https://twitter.com/sehurlburt/) who [asked people to help](https://twitter.com/sehurlburt/status/889004724669661184)!\n\n----"

output += "\n\n|User|Profile Description|Tweet|"
output += "\n" + "|----|----|----|"

if result['statuses']:
    while True:
        # process results and output
        for x in range(0, len(result['statuses'])):
            # Two things being filtered here:
            #  - Retweets aren't from mentors (RT at beginning)
            #  - Most of the tweets less than ~45 characters aren't about mentorship
            if (result['statuses'][x]['text'].find('RT ') == -1) and (len(result['statuses'][x]['text']) > 45):
                # print('what', result['statuses'][x]['user']['screen_name'].encode('utf-8'))
                tweets[result['statuses'][x]['id']] = {
                    'text': result['statuses'][x]['text'],  #.encode('utf-8'),
                    'user': {
                        'id' : result['statuses'][x]['user']['id'],
                        'name' : result['statuses'][x]['user']['name'], # .encode('utf-8')
                        'profile' : 'https://twitter.com/' + result['statuses'][x]['user']['screen_name'], # .encode('utf-8')
                        'description' : result['statuses'][x]['user']['description']   #.encode('utf-8')
                    }
                }

                # add username + profile link
                output += "\n" + "[" + tweets[result['statuses'][x]['id']]['user']['name'] + "](" + tweets[result['statuses'][x]['id']]['user']['profile'] + ")" + "|"

                # add the description
                output += escape_text_for_table(tweets[result['statuses'][x]['id']]['user']['description']) + "|"

                # add tweet
                output += make_twitter_link_clickable(escape_text_for_table(tweets[result['statuses'][x]['id']]['text'])) + "|"

        # no more crawling if results were less than 100 in last call
        if len(result['statuses']) < 0:
            break
        else:
            # take the ID of last tweet we had, get everything until that one
            last_tweet_id = min(tweets.keys())
            result = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=100, max_id=last_tweet_id)
else:
    print("Incorrect result from Twitter")

with io.open("data/twitter_table.md", "w", encoding="utf-8") as outfile:
    outfile.write(str(output))  # .decode('utf-8')
