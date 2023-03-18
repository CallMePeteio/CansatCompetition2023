

from digitalio import DigitalInOut, Direction, Pull
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask import current_app
from flask import Flask

import adafruit_rfm9x
import logging
import sqlite3

import threading
import socket
import fcntl
import busio
import board 
import json 
import time


db = SQLAlchemy() # MAKES THE DB OBJECT
DB_NAME = "database.db" # DEFINES THE NAME OF THE DB
pathToDB = "/home/pi/code/instance/database.db" # THIS IS THE PATH TO THE DATABASE
pathToReciveJson = "/home/pi/code/instance/recive.json" # RECIVE JSON FULL PATH
pathToTransmitJson = "/home/pi/code/instance/transmit.json" # TRANSMIT JSON FULL PATH

TX_RX_sleep = 0.8 # THIS IS HOW MUTCH THE SCRIPT WILL SLEEP BETWEEN TRANSMITTING AND RECIVING
writeRecivedData = False # IF YOU SHOULD WRITE THE RECIVED DATA TO THE DB AND JSON FILE

"""
Level: NOTSET > DEBUG > INFO > WARNING > ERROR > CRITICAL
Value:   0    >  10   >  20  >    30   >  40   >  50
"""
from . loggingFont import formatFont
loggingLevel = 10 # DEFINES THE LOGGING LEVEL
logger = logging.getLogger() # MAKES THE LOGGING OBJECT
logger.setLevel(loggingLevel) # SETS THE LEVEL AS DEFINED ABOVE
logger = formatFont(logger)


currentIp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
currentIp.connect(("8.8.8.8", 80))
currentIp = currentIp.getsockname()[0]

# This is the current columns of the "telemData" table in the db
telemdataColumnsDB = ["id", "flightId", "time", "atmoTemp", "temperature", "humidity", "pressure", "accelX", "accelY", "accelZ", "rollDeg", "pitchDeg", "yawDeg", "flightTime"] # KEEPS TRACK OF THE COLUMNS IN THE TELEMETRY TABLE

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
radio = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0, baudrate=10000000) # baudrate=10000000

# Makes the data Lock
dataLock = threading.Lock() # KEEPS TRACK OF THE LOCK, TO ENSURE THAT THERE ISNT 2 SCRIPTS SIMUNANIUSLY READING/WRITING TO IT


def create_app(reciveData, transmitData):
    app = Flask(__name__)

    
    app.config['reciveData'] = reciveData # SETS THE RECIVE DATA TO A GLOBAL VARIABLE, THAT CAN BE ACSESSED ALONG THREADS AND HAS A LOCK FUNCTION
    app.config['transmitData'] = transmitData # SETS THE RECIVE DATA TO A GLOBAL VARIABLE, THAT CAN BE ACSESSED ALONG THREADS AND HAS A LOCK FUNCTION

    app.config['SECRET_KEY'] = 'hjshjhdjvgdfhgfsdghgfsdasaJKSDFGDRJKGHRR4784434ahkjshkjdhjslkjhjhlkhlkjhlhlh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .home import home
    from .graph import Graph
    from .telementry import telem

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(telem, url_prefix="/")
   
    from .physical import mainSwitch
    from .transmit import TX_RX_main
    from .models import User, GPSdata

    with app.app_context():
        db.create_all()



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, TX_RX_main, TX_RX_sleep, Graph, mainSwitch



#___________________________________________ FUNCTIONS ___________________________________________



"""
_________________________________________ readGobalFlaskVar ______________________________________

This function reads the global flask variable decleared in __init__.py, for example: app.config['reciveData'] = reciveData

If you want to read a variable from the global scope in flask this is the correct syntax: current_app.config['transmitData']
That line reads the "transmitData" golbal scope variable.

varName = This is the name of the variable you want to read, for example: "transmitData" if you want to read the transmitData variable (str)
dataLock = This is the lock that is beeing used for making sure that there isnt two scripts reading/writing to it in the same time. 

"""
def readGobalFlaskVar(varName, dataLock, log=True): 
    
    if log == True:
        logging.info(f"     Readed variable from {varName}") # LOGS THE OUTPUT

    with dataLock: # CHECKS IF THE LOCK IS OPEN, MEANING THAT THERE ISNT ANOTHER THREAD READING THE VARIABLE
        return current_app.config[varName] # RETURNS THE VARIABLE


"""
________________________________________ writeGobalFlaskVar ______________________________________

This function writes to a global flask variable decleared in __init__.py for example: app.config['reciveData'] = reciveData

if you want to read a variable from the global flask scope then this is the correct syntax: current_app.config['transmitData'].
When you have read a variable you can treat it as a normal variable, forexample current_app.config['transmitData'] = {"basic": {"isOn": 1, "exaple": 0}}.

dataPath = This is the path you want to read data from, NOTE the first index of this is the variable name. for example if i want to read a variable from the dict above: current_app.config['transmitData'] = {"basic": {"isOn": 1, "exaple": 0}}
then you need to input ["transmitData", "basic", "isOn"] (list)
value = This is what value you want to set is, in the example above if you want to change the variable to 0 then input 0. (str)
log = If you want to log the result, set to True on default (bool)

"""

def writeGobalFlaskVar(dataPath, value, dataLock, log=True): 

    def logAction(dataPath, value, log): 
        if log == True: #  CHECKS IF THE USER WANTS TO LOG THE ACTION
            logging.info(f"     Changed value in the global flask dict: {dataPath[0]} (path):{dataPath}, value: {value}")


    with dataLock: # IF THE LOCK IS FREE, MEANING THAT THERE ISNT ANOTHER SCRIPT READING/WRITING ON THIS VARIABLE
        if len(dataPath) == 2: # IF THERE IS 2 IN LENGTH OF THE DATAPATH
            current_app.config[dataPath[0]][dataPath[1]] = value # SETS THE VALUE OF THE DATAPATH TO THE VALUE INPUTTED
            logAction(dataPath, value, log) # LOGS THE ACTION

        elif len(dataPath) == 3: # IF THERE IS 3 IN LENGTH OF THE DATAPATH
            current_app.config[dataPath[0]][dataPath[1]][dataPath[2]] = value # SETS THE VALUE OF THE DATAPATH TO THE VALUE INPUTTED
            logAction(dataPath, value, log) # LOGS THE ACITON

        else: 
            raise Exception(f"the length of the datapath is wroong. inputted dataPath: {dataPath}") # IF THERE IS AN ERROR WITH THE DATA PATH
            





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

def selectFromDB(dbPath, table, argumentList, columnList, valueList, log=True):
      
    con = sqlite3.connect(dbPath) # CONNECTS TO THE DB
    cursor = con.cursor() # MAKES THE CURSOR, FOR SELECTING THE DATA

    getString = f"SELECT * FROM '{table}' {argumentList[0]} {columnList[0]}=?" # THIS IS THE STRING THAT IS GOING TO BE THE SQLITE COMMAND, ALREADY ADDED THE FIRST DATAPOINT

    if len(columnList) == len(valueList) or len(columnList) == 0 or len(valueList) == 0: # CHECKS IF THERE IS AN ERROR ON THE LENGTH OF THE INPUT PARAMETERS

        if len(columnList) >= 1: # IF THE INPUT PARAMETERS IS MORE THAN ONE, THEN IT ADDS THE AND SYNTAX AND THE PARAMETER TO THE GETSTRING VARIABLE
            for i, parameter in enumerate(columnList[1:]): # LOOPS OVER ALL OF THE EXTRA "AND" PARAMETERS
                getString += f"{argumentList[i+1]} {parameter}=?"



            cursor.execute(getString, (valueList)) # SELECTS ALL OF THE DATA ACCORDING TO THE PARAMETERS GIVEN ABOVE
            data = cursor.fetchall() # FETCHES ALL OF THE DATA

            if log == True: # IF THE RESULTS SHULD BE LOGGED
                logging.info(f"     Readed data from databace, command: {getString}{valueList}") # LOGS THE DATA
                logging.debug(f"    data recived: {data}")

            return data # RETURNS ALL OF THE DATA


        cursor.execute(getString, (valueList[0],)) # SELECTS ALL OF THE GPS DATA, WE DO THIS TWICE BECAUSE THE SYNTAX OF THIS SUCS ;(, I NEED TI HAVE TRHE COMMA THERE WHAT A SHIT LIBARY
        data = cursor.fetchall() # FETCHES ALL OF THE DATA, GIVEN THE PARAMETERS ABOVE

        if log == True: # IF THE RESULTS SHULD BE LOGGED
            logging.info(f"     Databace command (read): {getString}{valueList}") # LOGS THE DATA
            logging.debug(f"    data recived: {data}")

        con.close()
        return data # RETURNS ALL OF THE DATA

    else: 
      raise Exception(f"Parameter error when reading from DB, there has to be a value for eatch parameter. Parameters: {columnList}, Values: {valueList}") # IF THERE WAS A ERROR OF THE LENGHT OF THE DATA


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


"""
____________________________________________ getIpAdress _________________________________________
This function gets the current ip adress of the raspberry pi. This is a function because you can get ether eth0 or for example wlan0 ip adress. 

interFace = This is what interface ip adress you want to get, forexample if you want to get wlan0 then enter "wlan0" (str)
"""

def getIpAdress(interFace):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', interFace[:15])
        )[20:24])