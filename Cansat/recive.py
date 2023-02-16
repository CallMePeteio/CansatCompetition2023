






from . import pathToReciveJson, TX_RX_sleep, videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip, logging
from .camera import Camera
import time
import json

"""
{
    "basic": {
        "isOn": 0,
        "prime": 0,
        "reset": 0
    },
    "manualControl": {
        "activated": 0,
        "left": 0,
        "right": 0
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


def action(): 
    totalImageTaken = 1 # KEEPS TRACK OF THE TOTAL IMAGES TAKEN, THE IMAGES WILL BE CALLED 1,2,3,4 SO THEY DONT OWERWRITE ETCHOTHER
    camera = Camera(videoPath, imgPath, videoRes, fps, imgScaleXY, imgFlip) # MAKES THE CAMERA OBJECT NOTE THE OBJECT CLASS IS IN "camera.py"


    with open(pathToReciveJson) as flie: # OPENS THE "recive.json" FILE
        data = json.load(flie) # LOADS THE DATA IN "recive.json" FILE

        try:
            manualControl = data["manualControl"]["activated"] # GETS IF YOU WANT TO ACTIAVE MANUAL CONTROL
            if manualControl == 1: # CHECKS IF THE VARIABLE IS 1. 1=True, 0=False
                manualControlLeft = data["manualControl"]["left"]
                manualControlRight = data["manualControl"]["right"]

                """
                MAKE TURN LOGIC
                """


            takePhoto = data["camera"]["photo"] # GETS IF YOU CLICKED THAT YOU WANTED TO TAKE A PICTURE
            if takePhoto == 1: # CHECKS IF THE VARIABLE IS 1.
                camera.takePhoto(str(totalImageTaken) + ".jpg") # TAKES THE PHOTO USING THE "Camera" OBJECT
                totalImageTaken += 1 # ADDS 1 TO THE TOTALIMAGE TAKEN COUNTER, THIS IS TO UPDATE THE NAME SO THE PICTURES DOSENT OWERWRITE ETCHOTHER
        except KeyError: 
            logging.error(f"There was an error processing the data in: recive.json, please check that there is no syntax error on the keys and that they exist")

 













