import requests
import json

subscription_key = '81ccca801c964b0c8ae708f993662afc'
assert subscription_key

face_api_url = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect'

# image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'
image_url ='https://pbs.twimg.com/profile_images/414924617/Willow.NewFace.jpg'

headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
print(json.dumps(response.json()))