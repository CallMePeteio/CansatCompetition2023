

from datetime import datetime

import threading
import sqlite3
import socket
import time
import json 

debug = False
DB_NAME = "database.db" # DEFINES THE NAME OF THE DB
pathToDB = "/home/pi/code/instance/database.db" # THIS IS THE PATH TO THE DATABASE
pathToReciveJson = "/home/pi/code/instance/recive.json" # RECIVE JSON FULL PATH
pathToTransmitJson = "/home/pi/code/instance/transmit.json" # TRANSMIT JSON FULL PATH

graphUpdateInterval = 5000 # DEFINES HOW MANY TIMES A MILISECOND THE GRAPHS SHOULD UPDATE (ms)
grafHostDict = {"temperature": ["0.0.0.0", "5200"], "tempPressure": ["0.0.0.0", "5100"], "humidity": ["0.0.0.0", "5300"], "pressure": ["0.0.0.0", "5400"], "gpsMap": ["0.0.0.0", "5500"], "orientation": ["0.0.0.0", "5600"]} # THIS KEEPS TRACK OF THE PORT AND IP ADRESS OF THE 

currentIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
currentIp.connect(("8.8.8.8", 80))
currentIp = currentIp.getsockname()[0]

telemdataColumnsDB = ["id", "flightId", "time", "atmoTemp", "temperature", "humidity", "pressure", "accelX", "accelY", "accelZ", "rollDeg", "pitchDeg", "yawDeg", "flightTime"] # KEEPS TRACK OF THE COLUMNS IN THE TELEMETRY TABLE


"""
NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE -  NOTE - NOTE - NOTE - 

The current code dousent account if there was a change of day, for time calcuation

NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - 

"""


"""
___________________________________________ selectFromDB _________________________________________
This function reads data from a sqlite databace, it is dynamic in the sens that you could add an unlimteted parameters and unlimeded values to fit those parameters
The sqlite3 command is strored in the variable "getString"

dbPath = This is the path to the databace you want to read data from. example: "F:\Scripts\Python\canSat\website\instance\database.db" (str)
table = This is the name of the table you want to read data from. example: "flightmaster" (str)
columnList = This is the list of parameters you want to add to the "getString" variable. for example if you want to get data from column "id" then input ["id"]. If you want to inpuut and AND statment then add it in the lsit. For example if you want from the column id  where the loginId = 1 then input: ["id", "loginId"]. The value will be added under
valueList = This is the list of values you add to the column list.
argument = This is the argument you want to do, forexample could you add AND.


"""

def selectFromDB(dbPath, table, argumentList, columnList, valueList):
      
    con = sqlite3.connect(dbPath) # CONNECTS TO THE DB
    cursor = con.cursor() # MAKES THE CURSOR, FOR SELECTING THE DATA

    getString = f"SELECT * FROM '{table}' {argumentList[0]} {columnList[0]}=?" # THIS IS THE STRING THAT IS GOING TO BE THE SQLITE COMMAND, ALREADY ADDED THE FIRST DATAPOINT

    if len(columnList) == len(valueList) or len(columnList) == 0 or len(valueList) == 0: # CHECKS IF THERE IS AN ERROR ON THE LENGTH OF THE INPUT PARAMETERS

      if len(columnList) >= 1: # IF THE INPUT PARAMETERS IS MORE THAN ONE, THEN IT ADDS THE AND SYNTAX AND THE PARAMETER TO THE GETSTRING VARIABLE
        for i, parameter in enumerate(columnList[1:]): # LOOPS OVER ALL OF THE EXTRA "AND" PARAMETERS
          getString += f"{argumentList[i+1]} {parameter}=?"


        cursor.execute(getString, (valueList)) # SELECTS ALL OF THE DATA ACCORDING TO THE PARAMETERS GIVEN ABOVE
        data = cursor.fetchall() # FETCHES ALL OF THE DATA
        return data # RETURNS ALL OF THE DATA


      cursor.execute(getString, (valueList[0],)) # SELECTS ALL OF THE GPS DATA, WE DO THIS TWICE BECAUSE THE SYNTAX OF THIS SUCS ;(, I NEED TI HAVE TRHE COMMA THERE WHAT A SHIT LIBARY
      data = cursor.fetchall() # FETCHES ALL OF THE DATA, GIVEN THE PARAMETERS ABOVE
      con.close()
      return data # RETURNS ALL OF THE DATA

    else: 
      raise Exception(f"Parameter error when reading from DB, there has to be a value for eatch parameter. Parameters: {columnList}, Values: {valueList}") # IF THERE WAS A ERROR OF THE LENGHT OF THE DATA



#____________________________________________ readJson ___________________________________________


def readJson(dataPath, jsonPath, intToBool=False, log=True):

    for i in range(int(10 * 10)): # THE READ JSON SCRIPT TRIES A COUPLE OF TIMES IF THE DATA IN THE JSON FILE IS EMPTY, THIS IS BECAUSE MOST OF THE TIME THE REASON BECAUSE IT IS EMPTY IS BECAUSE THERE IS SOMEONE WRITING TO IT
        try:
            with open(jsonPath, "r+") as inFile: # OPENS THE FILE THAT YOU WANT TO READ

                jsonData = json.load(inFile) # LOADS THE JSON

                try:
                    for path in dataPath: # LOOPS OVER THE PATH IN THE DATA PATH, JSONDATA IS REWRITTEN TO MAKE THE JSON PATH DYNAMIC
                        jsonData = jsonData[path]
                except:
                    raise Exception(f"Wrong jsonData path entered, path: {dataPath}") # IF THERE IS AN ERROR WITH FINDING THE PATH



                if intToBool == True: # IF YOU WANT TO CONVERT BOOL TO INTEGER
                    if jsonData == 0: # IF JSON DATA IS 0
                        jsonData = False # SET THE DATA AS FALSE
                    elif jsonData == 1: # IF THE DATA IS 1
                        jsonData = True # SET THE DATA AS TRUE
                    else: 
                        raise Exception(f"    The data: {jsonData} cannot be converted to bolean, because the data isnt 0 or 1") # MAKES AN ERROR IF THE DATA RECIVED IS WRONG

                return jsonData # RETURNS THE DATA
        except:
           pass

"""
___________________________________________ timeToMinutes ________________________________________
This function turns a HR:MIN:SEC time format into minutes, this is used to calclate how mutch time has elapsed since the cansat has started, just take the endtime  minus the startTime

time = This is the current time in hr:min:sec format (str)
currentTime = This is if you want to get the current time
"""
def timeToMinutes(time, currentTime=False): 
  if currentTime == False: 
    hr, min, sec = time.split(':')
    minutes = (float(hr) * 60) + (float(sec) * 0.0166667) + float(min)

  else: 
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    hr, min, sec = currentTime.split(':')

    minutes = (float(hr) * 60) + (float(sec) * 0.0166667) + float(min)

  return minutes

