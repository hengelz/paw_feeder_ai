# https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/
# https://myfirstproject-dedfc-default-rtdb.firebaseio.com/
# https://docs.thunkable.com/v/snap-to-place/realtime-db
# https://medium.com/@abdelhedihlel/upload-files-to-firebase-storage-using-python-782213060064 
 
import firebase_admin
import time
from time import strftime
from firebase_admin import credentials
from firebase_admin import db, storage

cred = credentials.Certificate("/home/hengelz/Projects/STEM/firebaseServiceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://myfirstproject-dedfc-default-rtdb.firebaseio.com/', 
                                    'storageBucket': 'myfirstproject-dedfc.appspot.com'})

ref = db.reference("/")

isFeederActive = False
lastRunTime = None

# Create database structure
def loadTestData():
    import json
    with open("/home/hengelz/Projects/STEM/feeder_variables.json", "r") as f:
        file_contents = json.load(f)
    ref.set(file_contents)

def getDBVariableValue(variableName):
    # Get value of a variable
    ref = db.reference(variableName)
    return ref.get()

def setDBVariableValue(variableName, value):
    # Set value of a variable
    ref = db.reference(variableName)
    ref.set(value)

def uploadImage():
    fileName = "ferrari.jpg"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    # Opt : if you want to make public access from the URL
    blob.make_public()
    print("your file url", blob.public_url)
    print('done with storage bucket')

def printFeederInfo():
    print('isFeederActive', getDBVariableValue('isFeederActive'))
    print('lastRunTime', getDBVariableValue('lastRunTime'))

def testVariableSettings():
    isActive = getDBVariableValue('isFeederActive')
    print('isFeederActive:%s' % isActive)

    setVariableValue('isFeederActive', not isActive)
    isActive = getDBVariableValue('isFeederActive')
    print('isFeederActive:%s' % isActive)

    ref = db.reference('lastRunTime')
    print(ref.get())

def runFeeder():
    lastRunTime=strftime("%I:%M %p")
    setDBVariableValue('lastRunTime', lastRunTime)
    isFeederActive = True
    setDBVariableValue('isFeederActive', isFeederActive)
    # Do feeder run
    time.sleep(10)
    isFeederActive = False
    setDBVariableValue('isFeederActive', isFeederActive)

#printFeederInfo()
runFeeder()

print('done with testing RealtimeDB')




