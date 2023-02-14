
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import readJson, writeJson
from . import pathToTransmitJson
from . import logging


import json

home = Blueprint('home', __name__)





"""
__________________________________________ button Dict __________________________________________
This dict is written to optemise the lines of code and development of the button page on the home page. 
The dictionary saves the location of the buttons, forexample on the first basicOn button:

"basicOn": {"htmlIdentifier": ["basic", "turnOnCansat"], "jsonWritePathData": ["basic", "isOn", 1]},
<button class="btn btn-primary m-1 button w-40" name="basic" value="turnOnCansat">On</button>

The algorythm seartches for a tag with name "basic" and value of "turnOnCansat". as you can see above. 
Inside of the dictionary is there also a key called: "jsonWritePathData" This where and what value you want to write to, in the transmit.json file.

This is forexample the "basic" section of transmit.json:
{
    "basic": {
        "isOn": 0,
        "prime": 0,
        "reset": 0
    },

if i want when the button is clicked as defined above, to change the value isOn, then the correct path to find inside the json is: ["basic", "isOn", 1]. the 1 is the value you want to change to
To recap: 

htmlIdentifier is to find the button in the html
jsonWritePathData is the path and the value you want to change to.


NOTE YOU NED TO HAVE DIFFRENT KEYS FOR THE DICTIONARY, FOREXAMPLE YOU CANT HAVE ANOTHER "basicOn" key.

"""

btnDict = {
#______________________________________ Basic BTN Handeling ______________________________________
	"basicOn": {"htmlIdentifier": ["basic", "turnOnCansat"], "jsonWritePathData": ["basic", "isOn", 1]},
	"basicOff": {"htmlIdentifier": ["basic", "turnOffCansat"], "jsonWritePathData": ["basic", "isOn", 0]},
	"basicPrime": {"htmlIdentifier": ["basic", "primeCansat"], "jsonWritePathData": ["basic", "prime", 1]},
	"basicReset": {"htmlIdentifier": ["basic", "resetCansat"], "jsonWritePathData": ["basic", "reset", 1]},

#______________________________________ Misc BTN Handeling _______________________________________
	"miscBeeper": {"htmlIdentifier": ["misc", "beeper"], "jsonWritePathData": ["miscFunctions", "beeper", 1]},
	"miscLights": {"htmlIdentifier": ["misc", "lights"], "jsonWritePathData": ["miscFunctions", "lights", 1]},
	"miscPrime": {"htmlIdentifier": ["misc", "prime"], "jsonWritePathData": ["miscFunctions", "reset", 1]},
	"miscReset": {"htmlIdentifier": ["misc", "reset"], "jsonWritePathData": ["miscFunctions", "reset", 1]},

#_____________________________________ Camera BTN Handeling ______________________________________
	"cameraStart": {"htmlIdentifier": ["camera", "startVid"], "jsonWritePathData": ["camera", "startVid", 1]},
	"cameraStop": {"htmlIdentifier": ["camera", "stopVid"], "jsonWritePathData": ["camera", "startVid", 0]},
	"cameraPhoto": {"htmlIdentifier": ["camera", "photo"], "jsonWritePathData": ["camera", "photo", 1]},

#_____________________________________ Control BTN Handeling _____________________________________
	"controlLeft": {"htmlIdentifier": ["manualControl", "left"], "jsonWritePathData": ["manualControl", "left", 1]},
	"controlRight": {"htmlIdentifier": ["manualControl", "right"], "jsonWritePathData": ["manualControl", "right", 1]},
	"controlActivate": {"htmlIdentifier": ["manualControl", "actiaveManual"], "jsonWritePathData": ["manualControl", "activated", 1]},
	"controlDeactivate": {"htmlIdentifier": ["manualControl", "deAcviateManual"], "jsonWritePathData": ["manualControl", "activated", 0]}
}




@home.route("/", methods=["POST", "GET"])
@login_required
def renderHome():
    print() # TO MAKE THE LOGGINGS READEBLE


    if request.method == "POST": # IF THERE IS A POST REQUEST

#_________________________________________  BTN Handeling ________________________________________

        for keys, value in btnDict.items(): # LOOPS OVER ALL OF THE ITEMS IN THE BTN DICT
            id = value["htmlIdentifier"] # FINDS THE HTML IDENTYFIER
            data = value["jsonWritePathData"] # FINDS THE DATA PATH AND THE VALUE YOU WANT TO CHANGE TO

            if request.form.get(id[0]) == id[1]: # CHECKS IF YOU WANT TO TURN ON THE CANSAT
                logging.info(f"     The {id[1]} button was pressed!") # LOGS THE OUTPUT
                writeJson([data[0], data[1]], data[2], pathToTransmitJson) # SETS THE "isOn" KEY IN THE JSON FILE TO 1


    

    if request.method == "GET": 
        pass

    onCansat = readJson(["basic", "isOn"], pathToTransmitJson, intToBool=True) # CHECKS IF THE CANSAT IS ON
    startVideo = readJson(["camera", "startVid"], pathToTransmitJson, intToBool=True) # CHECKS IF THE USER WANTS TO START RECORDING VIDEO

    videoLength = readJson(["camera", "videoLength"], pathToTransmitJson) # GETS THE VIDEO LENGTH FROM THE transmit.json FILE

    print() # TO MAKE THE LOGGINGS READEBLE
    return render_template("home.html", user=current_user, cameraRecording=startVideo, videoText=videoLength, online=onCansat)