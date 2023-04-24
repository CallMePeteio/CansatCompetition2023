






from . import videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip, logging, TX_RX_sleep, destinationGPS
from .camera import Camera

import RPi.GPIO as gpio

import threading
import time
import json
import math

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


def action(reciveData, gpsData):
    totalImageTaken, totalVideoTaken,  hasTakenPhoto, hasStartedVideo,  prevDeg, i = 1, 1, False, False, 90, 0 # KEEPS TRACK OF THE TOTAL IMAGES TAKEN, THE IMAGES WILL BE CALLED 1,2,3,4 SO THEY DONT OWERWRITE ETCHOTHER
    camera = Camera(videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip) # MAKES THE CAMERA OBJECT NOTE THE OBJECT CLASS IS IN "camera.py"


    while True:
        i+=1
        try:
            manualControl = reciveData["manualControl"]["activated"] # GETS IF YOU WANT TO ACTIAVE MANUAL CONTROL
            if manualControl == "1": # CHECKS IF THE VARIABLE IS 1. 1=True, 0=False

                turnDeg = float(reciveData["manualControl"]["degrees"]) # GETS THE REQUESTED DEGREES
                if turnDeg != prevDeg: # IF THE REQUESTED DEGREES IS NOT THE SAME DEG
                    print(turnDeg)
                    setAngle(turnDeg, prevDeg, 1) # MOVES THE SERVO
                    prevDeg = turnDeg # UPDATES THE "prevDeg" VARIABLE
            
            elif str(i)[len(str(i)) -1] == "0": # IF THE LAST CHARACTER OF I == "0" (EVRY 10 TIMES)
                bearing = calculateCompasBearing((gpsData[0], gpsData[1]), destinationGPS)
                distance = calculateDistanceHome((gpsData[0], gpsData[1]), destinationGPS)
                print(bearing, distance)
                #setAngle()

                

            takePhoto = reciveData["camera"]["photo"] # GETS IF YOU CLICKED THAT YOU WANTED TO TAKE A PICTURE)
            if takePhoto == "1": # CHECKS IF THE VARIABLE IS 1.
                if hasTakenPhoto == False: # CHECKS IF THE USER HAS ALREADY TAKEN A PHOTO
                    camera.cameraStart() # STARTS THE CAMERA
                    camera.takePhoto(str(totalImageTaken) + ".jpg") # TAKES THE PHOTO USING THE "Camera" OBJECT
                    totalImageTaken += 1 # ADDS 1 TO THE TOTALIMAGE TAKEN COUNTER, THIS IS TO UPDATE THE NAME SO THE PICTURES DOSENT OWERWRITE ETCHOTHER
                    hasTakenPhoto = True
                    camera.cameraStop() # CLOSES THE CAMERA
                    logging.info(f"     Sucsesfully tok a photo: {str(totalImageTaken-1) + '.jpg'}")
            else:
                hasTakenPhoto = False


            
            startVideo = reciveData["camera"]["startVid"]
            if startVideo == "1": # IF THE USER WANTS TO START A VIDEO
                if hasStartedVideo == False: # IF HTE USER HASNT STARTED A VIDEO BEFORE
                    camera.cameraStart()
                    videoName = (str(totalVideoTaken) + ".avi")
                    print(videoName)
                    startVideoThread(camera, videoName)
                    hasStartedVideo = True
                    totalVideoTaken += 1
                    logging.info(f"     Started a video: {videoName}")


            else: 
                if hasStartedVideo == True:
                    hasStartedVideo = False
                    camera.record = False
                    camera.cameraStop()
                    logging.info(f"     Stoped a video: {videoName}")
                

                

            time.sleep(TX_RX_sleep)
        except Exception as error: 
            logging.error(f"There was an error in the recive.py script: \nError msg:     {error}")


def setAngle(angle, prevAngle, sleepMulyplier): 
    
    #servo.start(0) # STARTS THE PWM OUTPUT
    dutyCycle = (angle/180)*5 + 5 # CONVERTS THE REQUESTED DEGRESS TO BETWEEN A DUTYCYCLE OF 5 AND 10%
    gpio.output(servoPin, True) # SETS THE OUTPUT TO TRUE TO STOP INECCECARY JITTERING
    servo.ChangeDutyCycle(dutyCycle) # CHANGES THE SERVO POSITION TO THE REQUESTED DUTY CYCLE
    time.sleep(0.5) # SLEEPS A BIT TO MAKE THE SERVO MOVE
    gpio.output(servoPin, False) # STOPS THE OUTPUT PIN TO REMOVE UNECCECARY JITTERING
    servo.ChangeDutyCycle(0)
    #servo.stop() # STOPS THE PWM SIGNAL TO REDUCE JITTERING

def startVideoThread(camera, name):
    cameraThread = threading.Thread(target=camera.takeVideo, args=(name, False))
    cameraThread.start()


def calculateCompasBearing(pointA, pointB):

    """
    Calculates the initial compass bearing (direction) between two points
    on the Earth's surface using their GPS coordinates.

    Args:
        pointA: A tuple containing the latitude and longitude of the starting point (lat1, lon1)
        pointB: A tuple containing the latitude and longitude of the destination point (lat2, lon2)

    Returns:
        compass_bearing: The initial compass bearing in degrees, with values ranging from 0 to 360
    """

    lat1, lon1 = math.radians(pointA[0]), math.radians(pointA[1])
    lat2, lon2 = math.radians(pointB[0]), math.radians(pointB[1])

    dLon = lon2 - lon1

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    bearing = math.degrees(math.atan2(y, x))
    compass_bearing = (bearing + 360) % 360

    return compass_bearing


def calculateDistanceHome(coord1, coord2):
    """
    Calculate the great-circle distance between two points on the Earth's surface using the
    Haversine formula.

    Args:
        coord1: A tuple containing the latitude and longitude of the first point (lat1, lon1)
        coord2: A tuple containing the latitude and longitude of the second point (lat2, lon2)

    Returns:
        distance: The distance between the two points in meters
    """
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    R = 6371000  # Earth's radius in meters
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
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
