import dash
from dash import *
import plotly
import plotly.graph_objects as go
import numpy as np 

from funcVar import pathToDB, grafHostDict, selectFromDB, debug, graphUpdateInterval, currentIp

import pandas as pd 
import socket 
 



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


temperatureGraph = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def _create_fig():

    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [1]) # SELECTS ALL OF THE FLIGHT DATA WITH THE LOGINID OF 1
    latestFlightID = flightData[len(flightData) -1][0] # FINDS THE LATEST FLIGHTID
    flightData = selectFromDB(pathToDB, "telemdata", ["WHERE"], ["flightId"], [latestFlightID]) # SELECTS THE LATEST FLIGHT


    df = pd.DataFrame(flightData, columns=["id", "flightId", "time", "atmoPressure", "temperature", "flightTime"]) # WRAPS THE DATA IN A PANDAS DATAFRAME
    return [df["flightTime"], df["temperature"]] # RETURNS THE DATAFRAME, WITH THE DATA FLIGHTTIME AND TEMPERATURE IN A LIST


temperatureGraph.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph', figure = dict(
                data=[{'x': _create_fig()[0], # ADDS THE ALREADY ADDED DATA IF ANY
                       'y': _create_fig()[1], # ADDS THE ALREADY ADDED DATA IF ANY
                       'name': 'Altitude',
                        'mode': 'lines+markers',
                        'type': 'scatter'
                       }]
            )),
        dcc.Interval(
            id='interval-component',
            interval=graphUpdateInterval, # in milliseconds
            n_intervals=0
        )
    ])
)


@temperatureGraph.callback(Output('live-update-graph', 'extendData'),
              Input('interval-component', 'n_intervals'),
              [State('live-update-graph', 'figure')])
def update_graph_live(n, existing):

    data = {
        'time': [],
        'Altitude': []
    }


    flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [1]) # SELECTS ALL OF THE FLIGHT DATA WITH THE LOGINID OF 1
    latestFlightID = flightData[len(flightData) -1][0] # FINDS THE LATEST FLIGHTID
    flightData = selectFromDB(pathToDB, "telemdata", ["WHERE"], ["flightId"], [latestFlightID]) # SELECTS THE LATEST FLIGHT

    latestTime = flightData[len(flightData) -1][5] # FINDS THE LATEST TIME DATA
    latestTemp = flightData[len(flightData) -1][4] # FINDS THE LATEST TEMP DATA

    return dict(x=[[latestTime]], y=[[latestTemp]]) # RETURNS THE NEW DATA, IF THE DATA IS NOT EQUAL TO THE PAST DATA, THEN THE GRAF WILL NOT UPDATE


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    hostingDetails = grafHostDict["temperature"]

    isRunning = s.connect_ex((currentIp, int(hostingDetails[1]))) == 0
    if isRunning == False: 
        target=temperatureGraph.run_server(host=hostingDetails[0], port=hostingDetails[1], debug=debug)# RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)

