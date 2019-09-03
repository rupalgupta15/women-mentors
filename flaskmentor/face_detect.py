import requests
import json

subscription_key = ''  # TODO: Add subscription key
assert subscription_key


def get_gender_details(image_url):
    face_api_url = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect'
    # image_url ='https://pbs.twimg.com/profile_images/414924617/Willow.NewFace.jpg'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    print('response', response.json())
    if len(response.json()) > 0:
        # print('YO')
        gender_response = response.json()[0]['faceAttributes']['gender']
    else:
        gender_response = 'unknown'
    # print(json.dumps(response.json()))
    return gender_response


# get_gender_details('https://pbs.twimg.com/profile_images/414924617/Willow.NewFace.jpg')

## modified:
# 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
