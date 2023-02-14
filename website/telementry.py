
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user

from . import readJson, pathToTransmitJson
from . import pathToDB
from . import db

import plotly.express as px
import pandas as pd

import threading
import sqlite3
import folium
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

    localIpAdress = socket.gethostbyname(socket.gethostname())
    localIpAdress = "http://" + localIpAdress

    isOn = readJson(["basic", "isOn"], pathToTransmitJson, intToBool=True)
    return render_template('gps.html', user=current_user, online=isOn, localIpAdress=localIpAdress) # RETURNS THE HTML



#    m = folium.Map(location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13,no_wrap=True)
#
#    folium.Circle(
#        radius=100,
#        location=[45.5244, -122.6699],
#        popup="The Waterfront",
#        color="crimson",
#        fill=False,
#    ).add_to(m)
#
#    folium.CircleMarker(
#        location=[45.5215, -122.6261],
#        radius=50,
#        popup="Laurelhurst Park",
#        color="#3186cc",
#        fill=True,
#        fill_color="#3186cc",
#    ).add_to(m)
#
#    script = """
#        <script>
#            setInterval(function () {
#                location.reload();
#            }, 1000);
#        </script>
#    """
#
#    m._parent.header.add_child(folium.Element(script))
#
#    m.save("F:/Scripts/Python/canSat/website/website/templates/gpsMap.html")

#    return render_template("gpsMap.html", user=current_user)








@telem.route("/telemData", methods=["POST", "GET"])
@login_required
def telemData():

    localIpAdress = socket.gethostbyname(socket.gethostname())
    localIpAdress = "http://" + localIpAdress

    isOn = readJson(["basic", "isOn"], pathToTransmitJson, intToBool=True)
    return render_template("/telemData.html", localIpAdress=localIpAdress, user=current_user,online=isOn)
