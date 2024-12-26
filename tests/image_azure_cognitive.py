'''
    Test Azure cognitive services test
'''

'''
POST https://hzcomputervisionresource.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=Tags&language=en&gender-neutral-caption=False HTTP/1.1
Host: hzcomputervisionresource.cognitiveservices.azure.com
Content-Type: application/json
Ocp-Apim-Subscription-Key: 812a6d11472b44c38608674475e376de

{
  "url": "https://images.dog.ceo/breeds/germanshepherd/n02106662_590.jpg"
}

'''
import requests
import json
import pprint
api_url = "https://hzcomputervisionresource.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=Tags&language=en&gender-neutral-caption=False"
subscription_key = "812a6d11472b44c38608674475e376de"

def testURL():
    todo = {"url": "https://images.dog.ceo/breeds/germanshepherd/n02106662_590.jpg"} # real dog
    #todo = {"url": "https://vet.osu.edu/vmc/sites/default/files/images/dog_eating_food.jpg"} # dog eating food
    #todo = {"url": "https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/home-improvement/wp-content/uploads/2022/07/download-23.jpg"}
    #todo = {"url": "https://image.cnbcfm.com/api/v1/image/105940475-1559232349684190164-car-ferrari-sf90-stradale.jpg"}
    #todo = {"url": "https://content.instructables.com/FZ8/3I7B/LKB5XV2R/FZ83I7BLKB5XV2R.png"}
    #todo = {'url' : 'https://i0.wp.com/douglascuddletoy.com/wp-content/uploads/2022/08/2468.jpg'} # stuffed animal dog
    #todo = {'url': 'https://i.pinimg.com/736x/3d/08/79/3d0879ae3d4e0d009974e54bb60fbb2a.jpg'} # stuffed animal dog
    headers =  {"Content-Type":"application/json", "Ocp-Apim-Subscription-Key": subscription_key}
    theJson = json.dumps(todo)
    print("theJson:%s" % theJson)
    response = requests.post(api_url, data=json.dumps(todo), headers=headers)
    return response

def testImage():
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}

    #filepath = r"C:\Users\godle\Pictures\DogPictures\hakon3.JPG"  # dog 1
    #filepath = r"C:\Users\godle\Pictures\DogPictures\n02106662_590.jpg"  # dog 2
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_640x480_2.JPG"  # cup and keyboard
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_640x480.JPG"  # Hengel
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_640x480_3.JPG"  # Adam
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_640x480_4.JPG"  # Adam 2
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_640x480_5.JPG"  # Beata
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MEGA_3MP_JPEG_2048x1536.JPG" # coffe cup
    #filepath = r"C:\Users\godle\Pictures\DogPictures\MYPHOTO.JPG"  # Beata
    #filepath = r"/home/hengelz/Projects/STEM/ferrari.jpg"
    #filepath = r"/home/hengelz/Projects/STEM/test-python.jpg"
    filepath = r"/home/hengelz/Projects/STEM/images/lastPhoto.jpg" 
    #filepath = r"/home/hengelz/Projects/STEM/bowlWithFood.jpg"
    print(filepath)
    image_data = open(filepath, 'rb').read()

    response = requests.post(api_url, data=image_data, headers=headers)
    return response

def checkForDog(response):
    isDog = False
    tagsResult = response.json()['tagsResult']
    tagValues = tagsResult['values']
    for tag in tagValues:
        if 'dog' in tag['name']:
            isDog = True
    print('**** IS it a dog?:%s' % isDog)

def printTags(response):
    print('response:%s' % response.json())
    tagsResult = response.json()['tagsResult']
    tagValues = tagsResult['values']
    tagList = [tag['name'] for tag in tagValues]
    pprint.pprint(tagList)


def main():
    #response = testURL()
    response = testImage()
    printTags(response)
    #pprint.pprint(response.json())
    checkForDog(response)


main()
print('done')

