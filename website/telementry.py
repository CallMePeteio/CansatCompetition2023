
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
from netifaces import AF_INET

from . import readJson, pathToTransmitJson, currentIp
from . import pathToDB
from . import db

import plotly.express as px
import pandas as pd

import netifaces 
import threading
import sqlite3
import random
import plotly
import socket



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

    isOn = readJson(["basic", "isOn"], pathToTransmitJson, intToBool=True)
    return render_template('gps.html', user=current_user, online=isOn, gpsUrl=gpsUrl) # RETURNS THE HTML






@telem.route("/telemData", methods=["POST", "GET"])
@login_required
def telemData():

    graphUrl = "http://" + currentIp

    isOn = readJson(["basic", "isOn"], pathToTransmitJson, intToBool=True)
    return render_template("/telemData.html", graphUrl=graphUrl, user=current_user,online=isOn)
