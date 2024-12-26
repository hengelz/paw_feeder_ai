import gpiod
import time
from time import strftime
import firebase_admin
from firebase_admin import credentials, db, storage
from picamera2 import Picamera2, Preview

# Initialize releay line
RELAY_PIN = 17
chip = gpiod.Chip('gpiochip4')
relay_line = chip.get_line(RELAY_PIN)    
relay_line.request(consumer="RELAY", type=gpiod.LINE_REQ_DIR_OUT)

# Initialize Button line
BUTTON_PIN = 6
push_button_line = chip.get_line(BUTTON_PIN)
push_button_line.request(consumer="PUSH_BUTTON", type=gpiod.LINE_REQ_DIR_IN)

# Initialize Led line
LED_PIN = 21
led_line = chip.get_line(LED_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
led_line.set_value(0)

# Initialize feeder state variables
isFeederActive = 'No'
webButtonToRunFeeder = False
webPhotoButton = False
photoFileName = '/home/hengelz/Projects/STEM/images/lastPhoto.jpg'

def initializeCloud():
    try:
        cred = credentials.Certificate("/home/hengelz/Projects/STEM/firebaseServiceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://myfirstproject-dedfc-default-rtdb.firebaseio.com/', 
                                        'storageBucket': 'myfirstproject-dedfc.appspot.com'})
        setDBVariableValue('isFeederActive', 'No')
        setDBVariableValue('webButtonToRunFeeder', False)
        setDBVariableValue('webPhotoButton', False)    
        db.reference('webButtonToRunFeeder').listen(webButtonPressed)
        db.reference('webPhotoButton').listen(webPhotoButtonPressed)
    except:
        print('Error initialiazing cloud')
    
def turnOnMotor():
    print('turning ON motor')
    relay_line.set_value(1)
    setDBVariableValue('isFeederActive', 'Yes')
    led_line.set_value(1)

def turnOffMotor():
    print('turning OFF motor')
    relay_line.set_value(0)
    setDBVariableValue('isFeederActive', 'No')
    setDBVariableValue('webButtonToRunFeeder', False)
    webButtonToRunFeeder = False
    led_line.set_value(0)

def getDBVariableValue(variableName):    
    ref = db.reference(variableName)
    return ref.get()

def setDBVariableValue(variableName, value):
    try:
        ref = db.reference(variableName)
        ref.set(value)
    except:
        print('Error while setting variable %s please check cloud connection' % variableName)

def webButtonPressed(event):
    global webButtonToRunFeeder    
    if event.data == True:
        webButtonToRunFeeder = True

def webPhotoButtonPressed(event):
    global webPhotoButton  
    if event.data == True:
        webPhotoButton = True

def takePhoto():
    try:
        picam = Picamera2()
        #config = picam.create_preview_configuration()
        config = picam.create_still_configuration()
        picam.configure(config)
        #picam.start_preview(Preview.QTGL) ### commenting out as it is giving troubles after change on settings to the window remote connect(DRMDevice in /etc/X11/xrdp/xorg.conf) and not needed anyways :)
        picam.start()
        time.sleep(2)
        picam.capture_file(photoFileName)
        picam.close()
        uploadImage('lastPhoto', photoFileName)
    except Exception as error:
        print('Error while taking the picture:%s' % error)
        
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
    blob.make_public()
    
    setDBVariableValue('imageCounter', imageCounter)
    setDBVariableValue('imagePublicUrl', blob.public_url)

    print("photo public URL:", blob.public_url)
    print('done storing photo in storage bucket')

def runFeeder():
    print('running feeder')        
    lastRunTime=strftime("%A %x %I:%M %p")
    setDBVariableValue('lastRunTime', lastRunTime)                    
    # Run feeder for 10 seconds
    turnOnMotor()        
    time.sleep(10)
    turnOffMotor()
    print('finished running feeder')
     
def main():
    print('Starting Pet feeder')
    global webButtonToRunFeeder
    global webPhotoButton
    initializeCloud()
    turnOffMotor()
    time.sleep(5)
    
    while True:
        if webButtonToRunFeeder or push_button_line.get_value()==0: # Runs feeder and takes photo
            setDBVariableValue('webButtonToRunFeeder', False)
            webButtonToRunFeeder = False
            runFeeder()                
            takePhoto()
        elif webPhotoButton: # Only takes a photo if web button is pressed
            setDBVariableValue('webPhotoButton', False)                
            webPhotoButton = False
            takePhoto()
            
### Start program            
main()

