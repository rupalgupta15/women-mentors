from twitter import *
import os

# consumer_key = os.getenv("CONSUMER_KEY_TWITTER")
# consumer_secret = os.getenv("CONSUMER_SECRET_TWITTER")
# access_token = os.getenv("ACCESS_KEY_TWITTER")
# access_token_secret = os.getenv("ACCESS_SECRET_TWITTER")

consumer_key = "9jurSy2yLbPaGLPr3mBnoq61b"
consumer_secret = "8Ymv6VJAGvOAXD5F8upt3iLbdsFBkj3rauToRKgFXJrOdx5jpn"
access_token = "526834125-KNkrRzAiYGv7dcBnbg78VQ3eYWueGaxeXMwTOuXW"
access_token_secret ="ZdELv0MenDKsTXoef5sqyxd0MtZwtkCadVo9t9vUXOoZ1"

t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))  #, retry=True

# reply = t.search.tweets(q="https://twitter.com/sehurlburt/status/889004724669661184", count=50)
reply = t.search.tweets(q="https://twitter.com/nytimes/status/1129139682569261056", count=5)

reply_tweets = {}

print('result', reply)
print('WTF', len(reply))

# if reply['statuses']:  # If something is returned : this is a list of dictionaries
#     for i in range(0, len(reply['statuses'])):
#         # Removing replies that are retweets and less than 45 chars in length
#         print('YOOPO', reply['statuses'][i]['text'])
#         print('YOOPO', len(reply['statuses'][i]['text']) > 45)
#         print('WUHUHUU', reply['statuses'][i]['user']['description'].encode('utf-8'))
#         if (reply['statuses'][i]['text'].find('RT ') == -1) and (len(reply['statuses'][i]['text']) > 45):
#             print('look at this', reply['statuses'][i]['user']['id'])
            # reply_tweets[reply['statuses'][i]['id']] = {
            #     'text': reply['statuses'][i]['text'].encode('utf-8'),
            #     'user': {
            #         'id': reply['statuses'][i]['user']['id'],
            #         'name': reply['statuses'][i]['user']['name'].encode('utf-8'),
            #         'profile': 'https://twitter.com/' + reply['statuses'][i]['user']['screen_name'].encode('utf-8'),
            #         'description': reply['statuses'][i]['user']['description'].encode('utf-8')
            #     }
            # }
#
# print('reply_tweets', reply_tweets)