
from . import telemdataColumnsDB
from . import selectFromDB
from . import currentIp
from . import pathToDB

from dash import *

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import socket
import dash
import time





class Graph:
    def __init__(self, dbDataPath, dictDataPath, updateTime, port, updateData=None):

        self.updateData = updateData

        self.dbDataPath = dbDataPath
        self.dictDataPath = dictDataPath
        self.updateTime = updateTime*1000
        self.port = port



        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.graph = dash.Dash(__name__, external_stylesheets=self.external_stylesheets)

    
    def _create_fig(self):
        flightData = selectFromDB(pathToDB, "flightmaster", ["WHERE"], ["loginId"], [1], log=False)
        latestFlightID = flightData[len(flightData) - 1][0]
        flightData = selectFromDB(pathToDB, "telemdata", ["WHERE"], ["flightId"], [latestFlightID], log=False)

        df = pd.DataFrame(flightData, columns=telemdataColumnsDB)
        return [df[self.dbDataPath[0]], df[self.dbDataPath[1]]]

    def _initialize_layout(self):
        self.graph.layout = html.Div(
            html.Div([
                dcc.Graph(id='live-update-graph', figure=dict(
                    data=[{'x': self._create_fig()[0],
                           'y': self._create_fig()[1],
                           'name': 'Altitude',
                           'mode': 'lines+markers',
                           'type': 'scatter'
                           }])),
                dcc.Interval(id='interval-component', interval=self.updateTime, n_intervals=0)]))

    def _register_callbacks(self):
        @self.graph.callback(Output('live-update-graph', 'extendData'),
                             Input('interval-component', 'n_intervals'),
                             [State('live-update-graph', 'figure')])
        
        def update_graph_live(n, existing):
            latestTemp, latesTime, i = None, None, 0

            while latestTemp == None and latesTime == None: 
                latestTemp = self.updateData[self.dictDataPath[0]][self.dictDataPath[1][0]]
                latestTime = self.updateData[self.dictDataPath[2]] 

                if i != 0: 
                    time.sleep(self.updateTime/5000)
                    i+=1
            
            return dict(x=[[latestTime]], y=[[latestTemp]])

    def start(self, reciveData):
        self._initialize_layout()
        self._register_callbacks()

        self.updateData = reciveData

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            isRunning = s.connect_ex((currentIp, int(self.port))) == 0
            if not isRunning:
                print(f"------------------- Started: {self.dbDataPath[1]} -------------------")
                target = self.graph.run_server(host="0.0.0.0", port=self.port, debug=False)




#if __name__ == "__main__":
#    graph = Graph(None, ["flightTime", "temperature"], 5, 5100)
#    graph.start()
