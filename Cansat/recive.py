






from . import videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip, logging, TX_RX_sleep
from .camera import Camera

import RPi.GPIO as gpio

import time
import json

servoPin, freq = 16, 50
gpio.setmode(gpio.BCM)
gpio.setup(servoPin, gpio.OUT)
servo = gpio.PWM(servoPin, freq)
servo.start(0)
"""
{
    "basic": {
        "isOn": 0,
        "prime": 0,
        "reset": 0
    },
    "manualControl": {
        "activated": 0,
        "degrees": 0,
    },
    "miscFunctions": {
        "beeper": 0,
        "lights": 0,
        "x": 0,
        "y": 0
    },
    "camera": {
        "startVid": 0,
        "photo": 0,
        "videoLength": 0
    }
}
"""


def action(reciveData): 
    totalImageTaken, prevDeg = 1, 90 # KEEPS TRACK OF THE TOTAL IMAGES TAKEN, THE IMAGES WILL BE CALLED 1,2,3,4 SO THEY DONT OWERWRITE ETCHOTHER
    #camera = Camera(videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip) # MAKES THE CAMERA OBJECT NOTE THE OBJECT CLASS IS IN "camera.py"


    while True:
        try:
            manualControl = reciveData["manualControl"]["activated"] # GETS IF YOU WANT TO ACTIAVE MANUAL CONTROL
            if manualControl == "1": # CHECKS IF THE VARIABLE IS 1. 1=True, 0=False

                turnDeg = float(reciveData["manualControl"]["degrees"]) # GETS THE REQUESTED DEGREES
                if turnDeg != prevDeg: # IF THE REQUESTED DEGREES IS NOT THE SAME DEG
                    setAngle(turnDeg, prevDeg, 1) # MOVES THE SERVO
                    prevDeg = turnDeg # UPDATES THE "prevDeg" VARIABLE
                


            takePhoto = reciveData["camera"]["photo"] # GETS IF YOU CLICKED THAT YOU WANTED TO TAKE A PICTURE
            #if takePhoto == 1: # CHECKS IF THE VARIABLE IS 1.
                #camera.takePhoto(str(totalImageTaken) + ".jpg") # TAKES THE PHOTO USING THE "Camera" OBJECT
                #totalImageTaken += 1 # ADDS 1 TO THE TOTALIMAGE TAKEN COUNTER, THIS IS TO UPDATE THE NAME SO THE PICTURES DOSENT OWERWRITE ETCHOTHER

            time.sleep(TX_RX_sleep)
        except KeyError: 
            logging.error(f"There was an error processing the data in: rxData, please check that there is no syntax error on the keys and that they exist \nData:    {rxData}")


def setAngle(angle, prevAngle, sleepMulyplier): 
    
    #servo.start(0) # STARTS THE PWM OUTPUT
    dutyCycle = (angle/180)*5 + 5 # CONVERTS THE REQUESTED DEGRESS TO BETWEEN A DUTYCYCLE OF 5 AND 10%
    gpio.output(servoPin, True) # SETS THE OUTPUT TO TRUE TO STOP INECCECARY JITTERING
    servo.ChangeDutyCycle(dutyCycle) # CHANGES THE SERVO POSITION TO THE REQUESTED DUTY CYCLE
    time.sleep(0.5) # SLEEPS A BIT TO MAKE THE SERVO MOVE
    gpio.output(servoPin, False) # STOPS THE OUTPUT PIN TO REMOVE UNECCECARY JITTERING
    servo.ChangeDutyCycle(0)
    #servo.stop() # STOPS THE PWM SIGNAL TO REDUCE JITTERING


"""
while True: 
    setAngle(0, 10, 10)
    print("Angle 0")
    time.sleep(1)

    setAngle(90, 10, 10)
    print("Angle 180")
    time.sleep(1)

    #servo.ChangeDutyCycle(5)
    #print(0)
    #time.sleep(1)
    #servo.ChangeDutyCycle(10)
    #print(1)
    #time.sleep(1)
"""
