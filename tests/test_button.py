import gpiod
import time
import firebase_admin
from time import strftime
from firebase_admin import credentials
from firebase_admin import db, storage

# Initialize releay line
RELAY_PIN = 18
chip = gpiod.Chip('gpiochip4')
relay_line = chip.get_line(RELAY_PIN)    
relay_line.request(consumer="RELAY", type=gpiod.LINE_REQ_DIR_OUT)

def initializeCloud():
    cred = credentials.Certificate("/home/hengelz/Projects/STEM/firebaseServiceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://myfirstproject-dedfc-default-rtdb.firebaseio.com/', 
                                        'storageBucket': 'myfirstproject-dedfc.appspot.com'})
    isFeederActive = False
    setDBVariableValue('isFeederActive', isFeederActive)    
    
def turnOnMotor():
    print('turning ON motor')
    relay_line.set_value(1)
    setDBVariableValue('isFeederActive', True)

def turnOffMotor():
    print('turning OFF motor')
    relay_line.set_value(0)
    setDBVariableValue('isFeederActive', False)

       
def getDBVariableValue(variableName):    
    ref = db.reference(variableName)
    return ref.get()

def setDBVariableValue(variableName, value):    
    ref = db.reference(variableName)
    ref.set(value)
       
def runFeeder():
    try:
        lastRunTime=strftime("%I:%M %p")
        setDBVariableValue('lastRunTime', lastRunTime)        
                
        # Do feeder run
        turnOnMotor()        
        time.sleep(11)
        turnOffMotor()                                
        time.sleep(5)
    finally:
        turnOffMotor()        
    
def main():
    initializeCloud()
    
    try:
        turnOffMotor()
        time.sleep(5)        
        for i in range(3):
            print('running feeder')        
            runFeeder()
            print('finished running feeder')
    finally:
        relay_line.release()
    
    print('done')
    
main()
    
    
