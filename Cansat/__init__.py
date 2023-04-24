


from digitalio import DigitalInOut

import adafruit_rfm9x
import threading
import logging
import busio
import board 
import json
import time


from .loggingFont import formatFont
"""
Level: NOTSET > DEBUG > INFO > WARNING > ERROR > CRITICAL
Value:   0    >  10   >  20  >    30   >  40   >  50
"""
loggingLevel = 10 # DEFINES THE LOGGING LEVEL
logger = logging.getLogger() # MAKES THE LOGGING OBJECT
logger.setLevel(loggingLevel) # SETS THE LEVEL AS DEFINED ABOVE
logger = formatFont(logger) # MAKES THE LOGGING FORMAT AND COLORS


videoPath="/home/pi/code/CansatCompetition2023/cameraOutput/video/"
imgPath="/home/pi/code/CansatCompetition2023/cameraOutput/image/"
videoRes, fps, imgScaleXY, imgFlip = (640, 480), 10, (1,1), -1

TX_RX_sleep = 0.7
destinationGPS = (67.240672, 14.613711)

CS = DigitalInOut(board.CE1) # GETS WHAT THE CS PIN IS, AND MAKES IT AS A OBJ
RESET = DigitalInOut(board.D12) # THIS IS WHAT THE RESET PIN IS TO THE LORA RADIO, THIS IS NOT THE SAME PIN AS IN THE Rfm9x DOCUMENTATION, BECAUSE THE PI SENS HAT ALREADY UES THE PIN
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO) # MAKES THE SPI OBJECT
radio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0) # MAKES THE radio OBJECT FOR TRANSMISSION



def startApp(): 
    from .camera import Camera
    from .sensHat import writeSensorData
    from .writeData import TX_RX_main
    from .gpsModule import getGpsPos
    from .recive import action

    return writeSensorData, TX_RX_main, getGpsPos, action






"""
___________________________________________ writeJson ___________________________________________


This function writes json to a specified json file

dataPath = This is the path insdie the JSON file that you want to change the value to. for example in a json file that looks like this: {"basic": {"isOn": 0}}. If you want to change the value to IsOn then you need to input ["basic", "isOn"]. (list)
value = When you have specified the path, then you need to input what the value you want to chagne to. for example in the json above {"basic": {"isOn": 0}} you want to change the value 0 to 1. Input 1
jsonPath = This is the path to the json file. example: "D:/Scripts/Python/canSat/website/instance/transmit.json"
log = If you want the function to log out what variable is changed. NOTE the logging level will also block the logging.

"""
def writeJson(dataPath, value, jsonPath, log=True): 
    with open(jsonPath, "r+") as inFile: # OPENS THE FILE THAT YOU WANT TO CHANGE TO
        jsonData = json.load(inFile) # LOADS THE JSON

        if len(dataPath) == 1: # CHECKS IF YOU ONLY WANTED ONE KEY DEEP
            jsonData[dataPath[0]] = value # SETS THE DATA TO THE VALUE

            if log == True: #  CHECKS IF THE USER WANTS TO LOG THE ACTION
                logging.info(f"     Changed variable in transmit.json (path):{dataPath}, value: {value}")


        elif len(dataPath) == 2:  # CHECKS IF YOU ONLY WANTED TWO KEY DEEP
            jsonData[dataPath[0]][dataPath[1]] = value # SETS THE DATA TO THE VALUE

            if log == True: #  CHECKS IF THE USER WANTS TO LOG THE ACTION
                logging.info(f"     Changed variable in transmit.json (path):{dataPath}, value: {value}")

        else:
            raise Exception("the length of the datapath is wrong, supported length is 1 and 2") # MAKES AN ERROR IF YOU CHOSE MORE THAN 2 OR LESS THAN 1 IN THE KEY SEARCH

    with open(jsonPath, "w") as file: # OPENS THE FILE IN WRITE MODE 
        json.dump(jsonData, file) # DUMPS THE JSON TO THE JSON FILE



#____________________________________________ readJson ___________________________________________


def readJson(dataPath, jsonPath, intToBool=False, log=True):

    for i in range(int(TX_RX_sleep * 10)): # THE READ JSON SCRIPT TRIES A COUPLE OF TIMES IF THE DATA IN THE JSON FILE IS EMPTY, THIS IS BECAUSE MOST OF THE TIME THE REASON BECAUSE IT IS EMPTY IS BECAUSE THERE IS SOMEONE WRITING TO IT
        try:
            with open(jsonPath, "r+") as inFile: # OPENS THE FILE THAT YOU WANT TO READ

                jsonData = json.load(inFile) # LOADS THE JSON

                try:
                    for path in dataPath: # LOOPS OVER THE PATH IN THE DATA PATH, JSONDATA IS REWRITTEN TO MAKE THE JSON PATH DYNAMIC
                        jsonData = jsonData[path]
                except:
                    raise Exception(f"Wrong jsonData path entered, path: {dataPath}") # IF THERE IS AN ERROR WITH FINDING THE PATH

                if log == True: #  CHECKS IF THE USER WANTS TO LOG THE ACTION
                    logging.info(f"     Readed variable from transmit.json (path): {dataPath}. value: {jsonData}") # LOGS THE OUTPUT

                if intToBool == True: # IF YOU WANT TO CONVERT BOOL TO INTEGER
                    if jsonData == 0: # IF JSON DATA IS 0
                        jsonData = False # SET THE DATA AS FALSE
                    elif jsonData == 1: # IF THE DATA IS 1
                        jsonData = True # SET THE DATA AS TRUE
                    else: 
                        raise Exception(f"    The data: {jsonData} cannot be converted to bolean, because the data isnt 0 or 1") # MAKES AN ERROR IF THE DATA RECIVED IS WRONG

                return jsonData # RETURNS THE DATA
        except: 
            logging.error(f"     Error reading the data: {dataPath} From {jsonPath}. Total Tries: {i}")
            time.sleep(TX_RX_sleep/30) # SLEEPS A BIT TO LET THE OTHER SCRIPT WRITE THE DATA    



"""
_______________________________________ setGlobalVarDic _________________________________________

setGlobalVarDic - This function sets a global variable between threads, such as "gpsData", to the data gathered in the main function "getGpsPos".
The variable "gpsData" is also used in "sensHat.py" and "writeData.py" in different threads.

This is necessary because we cannot directly assign a value to the global variable "gpsData", instead we must explicitly index the variable to change it.

Parameters:
    inputDic: The data that you want to set to the global variable. This should be a dictionary.
    globalDic: The global variable that is used in other threads. This should be a dictionary.

Returns:
    None
"""


def setGlobalVarDic(inputDic, globalDic):
    for key, value in inputDic.items():
        if key in globalDic:
            if isinstance(globalDic[key], dict) and isinstance(value, dict):
                globalDic[key].update(value)
            else: 
                globalDic[key] = value

"""
def setGlobalVarDic(inputDic, globalDic):
    
    for key in globalDic.keys(): # LOOPS OVER ALL OF THE KEYS IN "globalVar"

        if isinstance(globalDic[key], dict): # IF THE KEY IS A DICT, MEANING THAT IT IS A NESTED DICTIONARY
            for nestedKey in globalDic[key].keys(): # LOOPS OVER ALL OF THE KEYS IN THE LISTED DICTIONARY

                if key in inputDic.keys(): # IF THE KEY THAT WE ARE LOOPING OVER EXISTS IN THE "inputVar" VARIABLE
                    if nestedKey in inputDic[key].keys(): # IF THE KEY THAT WE ARE LOOPING OVER EXISTS IN THE "inputVar" VARIABLE
                        globalDic[key][nestedKey] = inputDic[key][nestedKey] # SET THE DATA FROM "inputVar" to "globalVar"
                    else: 
                        break # STOPS THE FOR LOOP SO WE DONT LOOP OVER UNECCECARY ITEMS
                else:
                    break # STOPS THE FOR LOOP SO WE DONT LOOP OVER UNECCECARY ITEMS
                
        else: 
           globalDic[key] = inputDic[key] # SET THE DATA FROM "inputVar" to "globalVar"

"""
"""
_______________________________________ setGlobalVarList ________________________________________
"""

def setGlobalVarList(inputList, gloabList):
    for i, var in enumerate(inputList): # LOOPS OVER THE DATA GATHERED

        try:
            gloabList[i] = var # SETS THE VARIBALE IN GPS DATA TO THE VAR INDEXED I
        except IndexError: # IF THE INPUT LIST WAS SHORTER THAN THE GLOBAL LIST
            break # STOPS THE LOOP

