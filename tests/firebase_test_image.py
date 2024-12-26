import gpiod
import time
import firebase_admin
import time
from time import strftime
from firebase_admin import credentials
from firebase_admin import db, storage

# Initialize feeder state variables
isFeederActive = False
webButtonToRunFeeder = False

def initializeCloud():
    cred = credentials.Certificate("/home/hengelz/Projects/STEM/firebaseServiceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://myfirstproject-dedfc-default-rtdb.firebaseio.com/', 
                                        'storageBucket': 'myfirstproject-dedfc.appspot.com'})
    setDBVariableValue('isFeederActive', isFeederActive)
    #db.reference('webButtonToRunFeeder').listen(listener)
    setDBVariableValue('webButtonToRunFeeder', webButtonToRunFeeder)
    

def getDBVariableValue(variableName):    
    ref = db.reference(variableName)
    return ref.get()

def setDBVariableValue(variableName, value):    
    ref = db.reference(variableName)
    ref.set(value)
    
    
    
def uploadImage(cloudFileName, localFileName):
    imageCounter = getDBVariableValue('imageCounter')
    if imageCounter is None:
        imageCounter = 0
        
    bucket = storage.bucket()
    
    fullPath = cloudFileName + '_' + str(imageCounter) + '.jpg'
    
    blob = bucket.blob(fullPath)
    if blob.exists():
        blob.delete()
        
    imageCounter += 1
    fullPath = cloudFileName + '_' + str(imageCounter) + '.jpg'
    blob = bucket.blob(fullPath)
    
    blob.upload_from_filename(localFileName)
    # Opt : if you want to make public access from the URL
    blob.make_public()
    
    setDBVariableValue('imageCounter', imageCounter)
    setDBVariableValue('imagePublicUrl', blob.public_url)

    print("your file url", blob.public_url)
    print('done with storage bucket')

def listener(event):
    global webButtonToRunFeeder
    print('listener event.event_type: %s' % event.event_type)  # can be 'put' or 'patch'
    print('listener event.path:%s' % event.path)  # relative to the reference, it seems
    print('listener event.data:%s' % event.data)  # new data at /reference/event.path. None if deleted
    
    if event.data == True:
        webButtonToRunFeeder = True
        

def main():
    global webButtonToRunFeeder
    initializeCloud()
    
    
    #uploadImage('ferrari', 'ferrari.jpg')
    #uploadImage('lastPhoto', 'test-python.jpg')
    uploadImage('lastPhoto', 'ferrari.jpg')
    print('done')



main()
