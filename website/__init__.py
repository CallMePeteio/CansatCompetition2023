

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from sys import getsizeof
from flask import Flask
from os import path

import threading
import logging
import sqlite3
import json 


db = SQLAlchemy() # MAKES THE DB OBJECT
DB_NAME = "database.db" # DEFINES THE NAME OF THE DB
pathToDB = "E:\Scripts\Python\canSat\instance\database.db" # THIS IS THE PATH TO THE DATABASE
pathToReciveJson = "E:/Scripts/Python/canSat/instance/recive.json" # RECIVE JSON FULL PATH
pathToTransmitJson = "E:/Scripts/Python/canSat/instance/transmit.json" # TRANSMIT JSON FULL PATH

TX_RX_sleep = 1 # THIS IS HOW MUTCH THE SCRIPT WILL SLEEP BETWEEN TRANSMITTING AND RECIVING
writeRecivedData = False # IF YOU SHOULD WRITE THE RECIVED DATA TO THE DB AND JSON FILE

"""
Level: NOTSET > DEBUG > INFO > WARNING > ERROR > CRITICAL
Value:   0    >  10   >  20  >    30   >  40   >  50
"""
loggingLevel = 20 # DEFINES THE LOGGING LEVEL
logger = logging.getLogger() # MAKES THE LOGGING OBJECT
logger.setLevel(loggingLevel) # SETS THE LEVEL AS DEFINED ABOVE



def create_app():
    app = Flask(__name__)

    #app.config['FLASK_DEBUG'] = 1
    #app.config['DEBUG'] = True

    app.config['SECRET_KEY'] = 'hjshjhdjvgdfhgfsdghgfsdasaJKSDFGDRJKGHRR4784434ahkjshkjdhjslkjhjhlkhlkjhlhlh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .home import home
    from .telementry import telem



    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(telem, url_prefix="/")
   
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

    return app, TX_RX_main



#___________________________________________ FUNCTIONS ___________________________________________





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

        return data # RETURNS ALL OF THE DATA

    else: 
      raise Exception(f"Parameter error when reading from DB, there has to be a value for eatch parameter. Parameters: {columnList}, Values: {valueList}") # IF THERE WAS A ERROR OF THE LENGHT OF THE DATA




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