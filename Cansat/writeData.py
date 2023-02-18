



from . import pathToReciveJson, pathToTransmitJson, TX_RX_sleep, logging, loggingLevel, radio, readJson, pathToBackEndJson


import sqlite3
import random
import time 
import json 




"""
recive data Dict is 232 bytes
"""
"""
DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______

There is sometimes error when reading "recive.json", i think what is heppening is that it is empty. problem in "sendData()" function.

NOTE if yuu press the start vid button then the photo variable turns to 1, it looks like the cansat is reciving the right data. maby there is an uncompression issue

DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______DEBUG_______

"""


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
emptyDict = {"basic": {"isOn": None, "prime": None, "reset": None}, "manualControl": {"activated": None, "left": None, "right": None}, "miscFunctions": {"beeper": None, "lights": None, "x": None, "y": None}, "camera": {"startVid": None, "photo": None, "videoLength": None}}

def uncompressData(dictValues, emptyDict, seperator=","):
    dictValues = dictValues.split(seperator)
  
    emptyDict = {"basic": {"isOn": None, "prime": None, "reset": None}, "manualControl": {"activated": None, "left": None, "right": None}, "miscFunctions": {"beeper": None, "lights": None, "x": None, "y": None}, "camera": {"startVid": None, "photo": None, "videoLength": None}}
    emptyDict_ = emptyDict # SO THE SCIPT DOSENT OVERWRITE THE EMPTY DICTIONARY

    i=0 # KEEPS TRACK OF THE INDEX THAT WE ARE ON
    if len(dictValues) == len(emptyDict_) or True: # IF THE INPUT DATA IS VALID LENGTH
        for key in emptyDict_.keys(): # LOOPS OVER ALL OF THE KEYS IN THE DICTIONARY, THE "i" VARIABLE KEEPS TRACK OVER WHAT VALUE OF THE LSIT WE ARE ON

            if isinstance(emptyDict_[key], dict): # IF THERE IS A NESTED DICTIONARY, FOR EXAMPLE "acceleration": {"x": None, "y": None, "z": None}"
                for nestedKey in emptyDict_[key].keys(): # LOOPS OVER ALL OF THE KEYS IN THE PARENT KEY
                    emptyDict_[key][nestedKey] = dictValues[i] # SETS THAT VALUE TO THE VALUE IN THE LIST
                    i+=1 # ADDS ONE TO I, TO KEEP THE ORDER RIGHT ACCORDING TO THE "dictValues" LIST
            else: 
                emptyDict_[key] = dictValues[i] # SET THAT KEY TO THE CURRENT VALUE OF THE DICT VALUE
                i+=1 # ADDS ONE TO I, TO KEEP THE ORDER RIGHT ACCORDING TO THE "dictValues" LIST
        return emptyDict_ # RETURNS THE UNCOMPTESSED DTAA
    else: 
        raise Exception(f"The empty dict and the dictvalues is not the same lenght, plase check the input data, Len emptyDict: {len(emptyDict_)}, len dictValues: {len(dictValues)}")




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

    for i in range(int(TX_RX_sleep * 10)):

        try: 
            with open(pathToTransmitJson, "r+") as inFile: # OPENS THE TRANSMIT FILE
                jsonData = json.load(inFile) # LOADS THE FILE
                compresseData = compressData(jsonData)  # COMPRESSES THE DATA
                radio.send(bytes(compresseData, "utf-8")) # SENS THE COMPRESSED DATA DICT WITH THE rfm9x LORA RADIO
                break
    
        
        except ValueError: 
            logging.critical(f"     The 'transmit.json' file is empty, Tried to read it but got an error")

    return True
        

def reciveData():
    packet = radio.receive()

    if packet is not None: 
        
        try: 
            rxData = uncompressData(str(packet, "utf-8"), emptyDict)

            with open(pathToReciveJson, "w") as outFile: # OPENS THE RECIVE JSON FILE
                jsonData = json.dump(rxData, outFile) # OWERWRITES THE DATA IN THE JSON FILE
                return 1 # RETURNS 1, THIS IS TO CALULATE THE AVRAGE PACKET RECIVE RATE

        except UnicodeDecodeError: 
            logging.error("There was a problem unpacking the recived data")
   



    else:
        #logging.error(f"     The packet recived from the server is None!")
        return 0 # RETURNS 0, THIS IS TO CALULATE THE AVRAGE PACKET RECIVE RATE




def elapsedTime(startTimeFloat):
    return time.time() - startTimeFloat 


def TX_RX_main(gpsData):
    run, totalTime, totalRXpackets, i = True, 0, 0, 0

    time.sleep((TX_RX_sleep * 5) + TX_RX_sleep/2) # SLEEPS HALF THE TIME + 5 TIMES THE TOTAL TIME, SO THE "sensHat.py" SCRIPT CAN WRITE FETCH DATA TO THE "transmit.json" FILE, AND THE GPS MODULE CAN INITIALIZE

    while True: 
        startTime = time.time() # GETS THE CURRENT TIME
        run = sendData() # TRANSMITS THE DATA, FROM THE "transmit.json" FILE


        if elapsedTime(startTime) < TX_RX_sleep * 0.48: # IF THERE IS ENOUGH TIME LEFT TO RECIVE DATA
            rxPacket = reciveData() # RECIVES THE DATA
        else:
            rxPacket = 0
            logging.warning(f"     Didnt recive data to from the Server, because there wasnt enough time left to forfill the time constraint of {TX_RX_sleep}. Total elapsed time in this cycle: {elapsedTime(startTime)}")







        if elapsedTime(startTime) < TX_RX_sleep: # IF THERE IS ANY SPARE TIME LEFT
            time.sleep(TX_RX_sleep - elapsedTime(startTime)) # SLEEP THE SPARE TIME


        if loggingLevel <= 10: # IF YOU WANT TO LOG OUT THE RESULT
            i+=1 # ADDS 1 TO THE INDEX VARIABLE, THIS IS TO CALCULATE AVG TIME
            totalTime += elapsedTime(startTime) # ADDS THE ELAPSED TIME TO THE TOTALTIME VARIABLE
            totalRXpackets += rxPacket
            if str(i)[len(str(i)) -1] == "8": # IF I ENDS WITH "8" (EVRY 10TH TIME)
                logging.debug(f"     Avrage Transmit and recive time: {round(totalTime/i, 4)}") # LOG OUT THE AVG TIME
                logging.debug(f"     Avrage packet recive rate (%): {round((totalRXpackets/i)*100, 2)}") 
                logging.debug(f"     Number of sattelites connected: {gpsData[3]}")
                print()


        



    raise Exception("Error ending or reciving data (run=False)")





















