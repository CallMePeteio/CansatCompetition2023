


from . import readJson, pathToTransmitJson, pathToReciveJson, pathToDB, TX_RX_sleep, logging, loggingLevel, timeToMinutes, selectFromDB, db, writeRecivedData
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import GPSdata, Telemdata

from sys import getsizeof


import logging
import sqlite3
import random
import time 
import json 



"""

Send data Dict is 232 bytes


"""

def sendData():
    with open(pathToTransmitJson, "r+") as inFile: # OPENS THE TRANSMIT FILE
        jsonData = json.load(inFile) # LOADS THE FILE

    """
    EPIC SEND DATA SCIPT
    """
    time.sleep(random.uniform(0.3, 0.5))

    return True
        

def reciveData():
    """
    EPIC RECIVE DATA SCRIPT
    """
    time.sleep(random.uniform(0.3, 0.5))

    prevReciveData = {
        "gps": {
            "lat": 68.2075271897814,
            "lon": 15.1544641159597},
        "telemdata": {
            "atmoPressure": 11.05, 
            "temperature": 22.23}}

    recivedData = {
        "gps": {
            "lat": 67.2075271897814,
            "lon": 15.1544641159597},
        "telemdata": {
            "atmoPressure": 11.05, 
            "temperature": 22.23}}

    if reciveData != prevReciveData and writeRecivedData == True: # IF THERE IS NEW DATA

# -- GETS THE LAST FLIGHT ID AND THE START TIME OF THAT FLIGHT
        flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], ["1"], log=False) # GETS ALL OF THE PREVIUS FLIGHTS OF THE ADMIN
        latestFlightID = flightData[len(flightData) -1][0] # SELECTS THE LATEST FLIGHT ID (int)

        latestFlightStartTime = flightData[len(flightData) -1][2] # FINDS THE LATEST FLIGHT STARTTIME, RETURNS YEAR:MONTH HR:MIN:SEC
        latestFlightStartTime = latestFlightStartTime.split(" ")[1] # CONVERTS THE latestFlightStartTime TO HR:MIN:SEC
        flightStartMin = timeToMinutes(latestFlightStartTime) # CONVERTS THE LATEST FLIGHTSTARTTIME TO MINUTES


# -- CALCULATES THE ESTIMATED TIME SINCE THE CANSAT WAS STARTED
        currentFlightMin = timeToMinutes("_", currentTime=True) # GETS THE CURRENT FLIGHT TIME IN MINUTES
        estimatedFlightTime=currentFlightMin-flightStartMin # CALCULATES THE ESTMATED FLIGHT TIME

# -- WRITES THE DATA RECIVED TO THE DB
        gpsData = GPSdata(flightId=latestFlightID, lat=recivedData["gps"]["lat"], lon=recivedData["gps"]["lon"])
        telemData = Telemdata(flightId=latestFlightID, atmoPressure=recivedData["telemdata"]["atmoPressure"], temperature=recivedData["telemdata"]["temperature"], flightTime=estimatedFlightTime)

        db.session.add(gpsData)
        db.session.add(telemData)
        db.session.commit()


# -- WRITES THE GATHERED DATA TO THE RECIVE.JSON FILE (NOT USED)
        with open(pathToReciveJson, "w") as file: # OPENS THE FILE IN WRITE MODE 
            json.dump(recivedData, file) # DUMPS THE JSON TO THE JSON

        prevReciveData = reciveData  #NOTE NOTE NOTE NOTE NOTE NEEDS TO BE UNCOMMEDED TO WORK

    return True # RETURNS TRUE TO NOT STOP READING AND WRITING





def elapsedTime(startTimeFloat):
    return time.time() - startTimeFloat 


def TX_RX_main(app):
    with app.app_context(): # TO GET FULL PERMISSIONS TO READ AND WRITE TO DB
        run = True
        totalTime = 0
        i=0

        while True: 
            startTime = time.time()
            run = reciveData()


            if elapsedTime(startTime) < TX_RX_sleep * 0.6:
                run = sendData()
            else:
                logging.error(f"     Didnt send data to Cansat, because there wasnt enough time left to forfill the time constraint of {TX_RX_sleep}. Total elapsed time in this cycle: {elapsedTime(startTime)}")

            if elapsedTime(startTime) < TX_RX_sleep - 0.03: # ADD A BIT OF PADDING, BECAUSE IT TAKES A BIT OF TIME TO CAUSE THE SLEE
                time.sleep(TX_RX_sleep - elapsedTime(startTime))











            if loggingLevel <= 10: # IF YOU WANT TO LOG OUT THE RESULT
                i+=1 # ADDS 1 TO THE INDEX VARIABLE, THIS IS TO CALCULATE AVG TIME
                totalTime += elapsedTime(startTime) # ADDS THE ELAPSED TIME TO THE TOTALTIME VARIABLE
                if str(i)[len(str(i)) -1] == "8": # IF I ENDS WITH "1" (EVRY 10TH TIME)
                    logging.debug(f"     Avrage Transmit and recive time: {totalTime/i}") # LOG OUT THE AVG TIME


        raise Exception("Error ending or reciving data (run=False)")











