


import plotly.express as px
import pandas as pd

from funcVar import grafHostDict, selectFromDB, debug, pathToDB, currentIp
from dash import html
from dash import dcc
from dash import *

import random
import socket
import dash
import time


"""
NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - 

if you refresh the page then the code dosent show new points.
This is because the _ceate_fig() function dosent get called to create a new backdrop.
you have to restart the whole script to show the data

make a callback function that calls _create_fig() if there is a refresh?

NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - NOTE - 

"""

def _create_fig():
    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [1]) # SELECTS ALL OF THE FLIGHT DATA WITH THE LOGINID OF 1
    latestFlightID = flightData[len(flightData) -1][0] # FINDS THE LATEST FLIGHTID
    flightData = selectFromDB(pathToDB, "gpsdata", ["WHERE"], ["flightId"], [latestFlightID]) # SELECTS THE LATEST FLIGHT

    df = pd.DataFrame(flightData, columns=["id", "flightId", "time", "lat", "lon"]) # WRAPS THE DATA IN A PANDAS DATAFRAME

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="time", hover_data=["flightId"], # MAKES THE FIGURE, WITH THE DATA GATHERED ABOVE
                            color_discrete_sequence=["fuchsia"], zoom=3, height=600)
    fig.update_layout(mapbox_style="open-street-map") # SETS THE STYLE OF THE MAP
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # IDK WHAT THIS DOES ;)

    return fig



gpsMap = dash.Dash() # MAKES THE GPSMAP OBJECT
gpsMap.layout = html.Div([
    dcc.Graph(id="live-update-graph", figure=_create_fig()), # CREATES THE GRAF AND ASSIGNS THE ID OF live-update-graph

    dcc.Interval(id='interval-component',
            interval=1000, # SETS THE REFRESHRATE OF THE MAP (ms)
            n_intervals=0)

])


@gpsMap.callback(Output('live-update-graph', 'extendData'),
              Input('interval-component', 'n_intervals'),
              [State('live-update-graph', 'figure')])

def update_graph_live(n, existing):
    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [1]) # SELECTS ALL OF THE FLIGHT DATA WITH THE LOGINID OF 1
    latestFlightID = flightData[len(flightData) -1][0] # FINDS THE LATEST FLIGHTID
    flightGpsData = selectFromDB(pathToDB, "gpsdata", ["WHERE"], ["flightId"], [latestFlightID]) # SELECTS THE LATEST FLIGHT


    latestTime = flightGpsData[len(flightGpsData) -1][2] # FINDS THE LATEST TIME DATA
    latestLat = flightGpsData[len(flightGpsData) -1][3] # FINDS THE LATEST TEMP DATA
    latestLon = flightGpsData[len(flightGpsData) -1][4] # FINDS THE LATEST TEMP DATA

    return dict(lat=[[latestLat]], lon=[[latestLon]]) # RETURNS THE NEW DATA, IF THE DATA IS NOT EQUAL TO THE PAST DATA, THEN THE GRAF WILL NOT UPDATE



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    hostingDetails = grafHostDict["gpsMap"]

    isRunning = s.connect_ex((currentIp, int(hostingDetails[1]))) == 0
    if isRunning == False: 
        target=gpsMap.run_server(host=hostingDetails[0], port=hostingDetails[1], debug=debug)# RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)

