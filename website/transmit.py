


from . import readJson, pathToTransmitJson, pathToReciveJson, pathToDB, TX_RX_sleep, logging, loggingLevel, timeToMinutes, selectFromDB, db, writeRecivedData, radio
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import GPSdata, Telemdata

from sys import getsizeof

import threading
import logging
import random
import time 
import json 












"""
________________________________________ uncompressData _________________________________________

This function uncompresses the data from minimal charachters to a full sized dict, there is also a function to comress the data.

Forexmaple if you want to uncompress the tring: 
34.1,34.1,23.5,-0.0017278495943173766,12649492919445038,9652832746505737,

Then this script will output:
{"temprature": 34.1, "tempPressure": 34.1, "humidity": 23.5, "acceleration": {"x": -0.0017278495943173766, "y": 0.12649492919445038, "z": 0.9652832746505737}}

dictValues = This is the values that the empty dictonary will hold, aka the compressed string  
emptyDict = This is a empty dictorary that wil be filled in of the inputted compressed data NOTE you need to have the same LENGHT BETWEEN THE "dictValues" and the "emptyDict"
seperator = This is the seperator you want to have between the data

"""

emptyDict = {"gps": {"lat": None, "lon": None}, "telemData": {"temprature": None, "tempPressure": None, "humidity": None}, "acceleration": {"x": None, "y": None, "z": None}}

def uncompressData(dictValues, emptyDict, seperator=","):
    dictValues = dictValues.split(seperator)
    emptyDict = {"gps": {"lat": None, "lon": None}, "telemData": {"temprature": None, "tempPressure": None, "humidity": None}, "acceleration": {"x": None, "y": None, "z": None}}
    emptyDict_ = emptyDict # SO THE SCIPT DOSENT OVERWRITE THE EMPTY DICTIONARY


    i=0 # KEEPS TRACK OF THE INDEX THAT WE ARE ON
    try:
        for key in emptyDict_.keys(): # LOOPS OVER ALL OF THE KEYS IN THE DICTIONARY, THE "i" VARIABLE KEEPS TRACK OVER WHAT VALUE OF THE LSIT WE ARE ON

            if isinstance(emptyDict_[key], dict): # IF THERE IS A NESTED DICTIONARY, FOR EXAMPLE "acceleration": {"x": None, "y": None, "z": None}"
                for nestedKey in emptyDict_[key].keys(): # LOOPS OVER ALL OF THE KEYS IN THE PARENT KEY
                    emptyDict_[key][nestedKey] = dictValues[i] # SETS THAT VALUE TO THE VALUE IN THE LIST
                    i+=1 # ADDS ONE TO I, TO KEEP THE ORDER RIGHT ACCORDING TO THE "dictValues" LIST
            else: 
                emptyDict_[key] = dictValues[i] # SET THAT KEY TO THE CURRENT VALUE OF THE DICT VALUE
                i+=1 # ADDS ONE TO I, TO KEEP THE ORDER RIGHT ACCORDING TO THE "dictValues" LIST
        return emptyDict_ # RETURNS THE UNCOMPTESSED DTAA
    except IndexError:
        logging.critical(f"There was an error ucompessing the data recived \n dictValues: {dictValues} \n emptyDict: {emptyDict_}")

"""
_________________________________________ compressData __________________________________________

This function compresses a dict to the minimal characters, this is to improve the max frequency the rfm9x radios can communicate together, there is also a function to uncompress the data

Forexmaple if you want to compress the dict: 
{"temprature": 34.1, "tempPressure": 34.1, "humidity": 23.5, "acceleration": {"x": -0.0017278495943173766, "y": 0.12649492919445038, "z": 0.9652832746505737}}

Then this script will output:
34.1,34.1,23.5,-0.0017278495943173766,12649492919445038,9652832746505737,

dictionary = This is the dictonary of data you want to compress (dict)
seperator = This is the seperator you want to have between the data

"""

def compressData(dictionary, seperator=","): 
    rtnString = "" # THIS KEEPS TRACK OF THE ALREADY COMPRESSED DATA

    for values in dictionary.values(): # LOOPS OVER ALL OF THE VALUES IN THE INPUT DICTIONARY
        if isinstance(values, dict): # IT THE TYPE OF THE VALUE IS A DICT, MEANING THAT THERE IS A NESTED DICT EXAMPLE "{"temprature": 34.1, "acceleration": {"x": -0.0017278495943173766, "y": 0.12649492919445038, "z": 0.9652832746505737}}"
            for nestedValues in values.values(): # LOOP OVER ALL OF THE ITEMS IN THE VALUE'S DICT
                rtnString += str(nestedValues) + seperator # ADD THE VALUE TO THE "rtnString" VARIABLE, AND ADD A SEPERATOR EXAMPLE ","
        else:
            rtnString += str(values) + seperator # ADD THE VALUE TO THE "rtnString" VARIABLE, AND ADD A SEPERATOR EXAMPLE ","
    return rtnString # RETURNS THE VARIABLE





def sendData():
    with open(pathToTransmitJson, "r+") as inFile: # OPENS THE TRANSMIT FILE
        jsonData = json.load(inFile) # LOADS THE FILE
        compressedData = compressData(jsonData)
        radio.send(bytes(compressedData, "utf-8")) # SENDS THE DATA WITH THE "rfm9x" LORA RADIO MODULE

    return jsonData
        

def writeReciveData(recivedData):

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
    telemData = Telemdata(flightId=latestFlightID, atmoTemp=recivedData["telemData"]["tempPressure"], temperature=recivedData["telemData"]["temprature"], humidity=recivedData["telemData"]["humidity"], accelX=recivedData["acceleration"]["x"], accelY=recivedData["acceleration"]["y"], accelZ=recivedData["acceleration"]["z"], flightTime=estimatedFlightTime)

    db.session.add(gpsData)
    db.session.add(telemData)
    db.session.commit()


# -- WRITES THE GATHERED DATA TO THE RECIVE.JSON FILE (NOT USED)
    with open(pathToReciveJson, "w") as file: # OPENS THE FILE IN WRITE MODE 
        json.dump(recivedData, file) # DUMPS THE JSON TO THE JSON


    return recivedData # RETURNS TRUE TO NOT STOP READING AND WRITING





def elapsedTime(startTimeFloat):
    return time.time() - startTimeFloat 

def TX_RX_main(app): 
    with app.app_context(): # TO GET FULL PERMISSIONS TO READ AND WRITE TO DB
        while True: 

            hasStartedFlight = readJson(["basic", "runFlight"], pathToTransmitJson, intToBool=True, log=False)

            if hasStartedFlight == True:
                packet = radio.receive() # GETS DATA FROM THE RADIO
                if packet is not None: # IF THERE IS A PACKET

                    try:
                        recvieData = uncompressData(dictValues = str(packet, "utf-8"), emptyDict=emptyDict) # TRANSFORMES THE DATA TO A READEBLE DICTIONARY
                    except UnicodeDecodeError: 
                        logging.error("There was a problem unpacking the recived data")

                    writeReciveData(recvieData) # WRITES THE DATA TO THE DB

                    sendData() # SENDS THE DATA IN "transmit.json"
            else: 
                sendData() # SENDS THE DATA IN "transmit.json"







"""
def TX_RX_main(app): 
    with app.app_context(): # TO GET FULL PERMISSIONS TO READ AND WRITE TO DB
        totalTime, i = 0, 0

        while True: 
            startTime = time.time()

            reciveThread = threading.Thread(target=reciveDataFunc)
            reciveThread.start()

            if elapsedTime(startTime) < TX_RX_sleep * 0.8:
                sendThread = threading.Thread(target=sendData)
                sendThread.start()
            else: 
                logging.warning(f"     Didnt send data to Cansat, because there wasnt enough time left to forfill the time constraint of {TX_RX_sleep}. Total elapsed time in this cycle: {elapsedTime(startTime)}")
                



            if elapsedTime(startTime) < TX_RX_sleep: # ADD A BIT OF PADDING, BECAUSE IT TAKES A BIT OF TIME TO CAUSE THE SLEE
                try:    
                    time.sleep(TX_RX_sleep - elapsedTime(startTime))
                except: 
                    time.sleep(TX_RX_sleep - (elapsedTime(startTime) - 0.08))


            if loggingLevel <= 10: # IF YOU WANT TO LOG OUT THE RESULT
                    i+=1 # ADDS 1 TO THE INDEX VARIABLE, THIS IS TO CALCULATE AVG TIME
                    totalTime += elapsedTime(startTime) # ADDS THE ELAPSED TIME TO THE TOTALTIME VARIABLE
                    if str(i)[len(str(i)) -1] == "8": # IF I ENDS WITH "1" (EVRY 10TH TIME)
                        logging.debug(f"     Avrage Transmit and recive time: {totalTime/i}") # LOG OUT THE AVG TIME






def TX_RX_main(app):
    with app.app_context(): # TO GET FULL PERMISSIONS TO READ AND WRITE TO DB
        totalTime, i, sentData, reciveData = 0, 0, None, None

        while True: 
            startTime = time.time()
            reciveData = reciveDataFunc()


            if elapsedTime(startTime) < TX_RX_sleep * 0.6:
                sentData = sendData()
            else:
                logging.warning(f"     Didnt send data to Cansat, because there wasnt enough time left to forfill the time constraint of {TX_RX_sleep}. Total elapsed time in this cycle: {elapsedTime(startTime)}")



            if elapsedTime(startTime) < TX_RX_sleep: # ADD A BIT OF PADDING, BECAUSE IT TAKES A BIT OF TIME TO CAUSE THE SLEE
                try:    
                    time.sleep(TX_RX_sleep - elapsedTime(startTime))
                except: 
                    time.sleep(TX_RX_sleep - (elapsedTime(startTime) - 0.08))











            if loggingLevel <= 10: # IF YOU WANT TO LOG OUT THE RESULT
                i+=1 # ADDS 1 TO THE INDEX VARIABLE, THIS IS TO CALCULATE AVG TIME
                totalTime += elapsedTime(startTime) # ADDS THE ELAPSED TIME TO THE TOTALTIME VARIABLE
                if str(i)[len(str(i)) -1] == "8": # IF I ENDS WITH "1" (EVRY 10TH TIME)
                    logging.debug(f"     Avrage Transmit and recive time: {totalTime/i}") # LOG OUT THE AVG TIME
                    logging.debug(f"     Last data sent to Cansat: {sentData}")
                    logging.debug(f"     Last data recived from Cansat: {reciveData} \n")


        raise Exception("Error ending or reciving data (run=False)")


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
    
"""










