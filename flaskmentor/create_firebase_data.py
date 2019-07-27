# DO NOT RUN THIS CODE AGAIN AS FIREBAS MENTORS DATA HAS CHANGED
# This file is just used to modify the profile_image_url_https fiels from normal to actual

import json
from flaskmentor import fetch_twitter_img_url

firebase_data = {}
final_firebase_mentors = []

women_mentors = []
other_mentors = []

with open('../data/final_mentors.json', 'rb') as f:
    d = json.load(f)
    for k, v in d.items():
        normal_pic = v["profile_image_url_https"]
        original_profile_pic = fetch_twitter_img_url.return_original_profile_pic(normal_pic)
        v['original_profile_pic'] = original_profile_pic
        v['link_to_profile'] = "https://twitter.com/"+ v["screen_name"]
        if v['gender_val'] == 'female':
            women_mentors.append(v)
        else:
            other_mentors.append(v)

sorted_women = sorted(women_mentors, key=lambda i: i["followers_count"], reverse=True)
sorted_other = sorted(other_mentors, key=lambda i: i["followers_count"], reverse=True)

final_firebase_mentors = sorted_women
final_firebase_mentors.extend(sorted_other)

firebase_data = {item['id'] : item for item in final_firebase_mentors}

with open('../data/firebase_mentors_data.json', 'w') as fname:
    json.dump(firebase_data, fname, indent=4)

