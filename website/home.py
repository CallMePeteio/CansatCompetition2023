
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .models import Flightmaster
from datetime import datetime

from . import writeGobalFlaskVar
from . import readGobalFlaskVar
from . import selectFromDB
from . import dataLock
from . import pathToDB
from . import logging
from . import db


import sqlite3
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
	"basicSatrtFlight": {"htmlIdentifier": ["basic", "startFlight"], "jsonWritePathData": ["basic", "runFlight", 1]},
	"basicStopFlight": {"htmlIdentifier": ["basic", "stopFlight"], "jsonWritePathData": ["basic", "runFlight", 0]},

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

#---------------- BTN HANDELING
        for keys, value in btnDict.items(): # LOOPS OVER ALL OF THE ITEMS IN THE BTN DICT
            id = value["htmlIdentifier"] # FINDS THE HTML IDENTYFIER
            data = value["jsonWritePathData"] # FINDS THE DATA PATH AND THE VALUE YOU WANT TO CHANGE TO

            if request.form.get(id[0]) == id[1]: # CHECKS IF YOU WANT TO TURN ON THE CANSAT
                logging.info(f"     The {id[1]} button was pressed!") # LOGS THE OUTPUT
                writeGobalFlaskVar(["transmitData", data[0], data[1]], data[2], dataLock) #  SETS THE "isOn" KEY IN THE GLOBAL VARIABLE (FLASK) "transmitData" FILE TO 1

#---------------- ADDS A NEW FLIGHT IF THE USER CLICKED THE BUTTON
        startFlight = btnDict["basicSatrtFlight"]["htmlIdentifier"]
        if request.form.get(startFlight[0]) == startFlight[1]:
            
            now = datetime.now() # GETS THE CURRENT TIME
            currentTime = now.strftime("%Y-%m-%d %H:%M:%S") # CHANGES THE TIME FORMAT TO THE CORRECT FORMAT
            flightMake = Flightmaster(loginId=current_user.id,  startTime=currentTime) # MAKES A NEW FLIGT
            db.session.add(flightMake) # ADDS THE TABLE TO THE SESSION
            db.session.commit() # COMMITS THE SESSION
    


#---------------- SETS THE ENDTIME COLUMN IN THE FLIGHTMASTER TABLE (IF THE USER STOPS THE FLIGHT)
        startFlight = btnDict["basicStopFlight"]["htmlIdentifier"]
        if request.form.get(startFlight[0]) == startFlight[1]:

            con = sqlite3.connect(pathToDB) # CONNECTS TO THE DB
            cursor = con.cursor() # MAKES THE CURSOR, FOR SELECTING THE DATA

            flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [current_user.id]) # SELECS ALL OF THE DATA FROM FLIGHTMASTER WHERE LOGINID IS CURRENT USER.ID
            latestFlightID = flightData[len(flightData) -1][0] # GETS THE LATEST FLIGHT ID

            now = datetime.now() # GETS THE CURRENT TIME
            currentTime = now.strftime("%Y-%m-%d %H:%M:%S") # CHANGES THE TIME FORMAT TO THE CORRECT FORMAT

            cursor.execute("UPDATE 'flightmaster' SET endTime=? WHERE id=?", (currentTime, latestFlightID,))
            con.commit()
            con.close()


    onCansat = readGobalFlaskVar("transmitData", dataLock)["basic"]["isOn"]  # CHECKS IF THE CANSAT IS ON
    startVideo = readGobalFlaskVar("transmitData", dataLock)["camera"]["startVid"] # CHECKS IF THE USER WANTS TO START RECORDING VIDEO
    videoLength = readGobalFlaskVar("transmitData", dataLock)["camera"]["videoLength"]  # GETS THE VIDEO LENGTH FROM THE GLOBAL VARIABLE "transmitData" (json)

    print() # TO MAKE THE LOGGINGS READEBLE
    return render_template("home.html", user=current_user, cameraRecording=startVideo, videoText=videoLength, online=onCansat)