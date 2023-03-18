
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from . import readGobalFlaskVar, dataLock
from . import currentIp, selectFromDB
from . import pathToDB
from . import db

import plotly.express as px
import pandas as pd

import netifaces 
import sqlite3
import random




telem = Blueprint('telem', __name__)


@telem.route("/gps", methods=["POST", "GET"])
@login_required
def gps():
    con = sqlite3.connect(pathToDB) # CONNECTS TO THE DB
    cursor = con.cursor() # MAKES THE CURSOR, FOR SELECTING TABLES AND ROWS

    cursor.execute("SELECT * FROM 'gpsdata'") # SELECTS ALL OF THE GPS DATA
    gpsData = cursor.fetchall() # FETCHES ALL OF THE GPS DATA
    df = pd.DataFrame(gpsData, columns=["id", "loginId", 'time', 'lat','lon',]) # PLACES THE DATA IN A PANDA DATAFRAME

  
    lastPos = (df.tail(1))
 
    #fig.update_layout(center=px.layout.mapbox.Center(lat=lastPos["lat"], lon=lastPos["lon"]),) # ADDS MARGINS TO THE MAP

    gpsUrl = "http://" + currentIp


    
    isOn = readGobalFlaskVar("transmitData", dataLock, log=False)["basic"]["isOn"]
    if isOn == True:
        isOn = readGobalFlaskVar("transmitData", dataLock)["basic"]["runFlight"]

    con.close()  
    return render_template('gps.html', user=current_user, online=isOn, gpsUrl=gpsUrl) # RETURNS THE HTML






@telem.route("/telemData", methods=["POST", "GET"])
@login_required
def telemData():

    graphUrl = "http://" + currentIp


    isOn = readGobalFlaskVar("transmitData", dataLock, log=False)["basic"]["isOn"]
    if isOn == True:
        isOn = readGobalFlaskVar("transmitData", dataLock)["basic"]["runFlight"]

        

    return render_template("/telemData.html", graphUrl=graphUrl, user=current_user,online=isOn)



@telem.route("/telemDataRaw", methods=["POST", "GET"])
@login_required
def telemDataRaw(): 
    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], ["1"]) # GETS ALL OF THE PREVIUS FLIGHTS OF THE ADMIN
    dataTable = selectFromDB(pathToDB, "telemdata", ["WHERE"], ["flightId"], [len(flightData)])

    telemdataColumns = ["id", "flightId", "time", "atmoTemp", "temperature", "humidity", "pressure", "accelX", "accelY", "accelZ", "rollDeg", "pitchDeg", "yawDeg", "flightTimeMin"]
    df = pd.DataFrame(dataTable, columns=telemdataColumns)

    df.to_csv("/home/pi/code/instance/telemDataCsv.csv",index=False)

    return f"<p>{df}</p>"
 
