import requests
import json
import pprint
from .petfeeder_secrets import azure_subscription_key
azure_api_url = "https://hzcomputervisionresource.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=Tags&language=en&gender-neutral-caption=False"

print('azure_subscription_key',azure_subscription_key)
def getImageDescription():
    response = None
    try:
        headers = {'Ocp-Apim-Subscription-Key': azure_subscription_key,
                   'Content-Type': 'application/octet-stream'}

        filepath = r"/home/hengelz/Projects/STEM/images/lastPhoto.jpg" 
        image_data = open(filepath, 'rb').read()
        response = requests.post(azure_api_url, data=image_data, headers=headers)
    except Exception as error:
        print('Error getting image description: %s' + error)
    return response

def checkForFood(response):
    wordsToSearch = ['food', 'candy', 'color', 'cereal']
    hasFood = 'No'
    if response:
        tagsResult = response.json()['tagsResult']
        tagValues = tagsResult['values']
        for tag in tagValues:
            for word in wordsToSearch:                
                if word in tag['name']:
                    hasFood = 'Yes'
                    print('Has food in the plate? %s' % hasFood)
                    return hasFood
    return hasFood

def getPhotoLabels(response):
    tagNames = None
    if response:
        tagsResult = response.json()['tagsResult']
        tagValues = tagsResult['values']
        tagNames = [tag['name'] for tag in tagValues]
        tagNames = ', '.join(tagNames)
    return tagNames
    
def test():
    response = getImageDescription()
    checkForFood(response)
    print(getPhotoLabels(response))
    
#test()