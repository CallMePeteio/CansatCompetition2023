
import sys
import os

from website import create_app
from makeGraph import createGraphs
#from graphs import start

import subprocess
import threading
import logging
import time
import sys
import os

#from website.graphWebsites.main import start





reciveData = {'gps': {'lat': None, 'lon': None}, 'telemData': {'temprature': None, 'tempPressure': None, 'humidity': None, 'pressure': None}, 'acceleration': {'x': None, 'y': None, 'z': None}, 'orientation': {'roll': None, 'pitch': None, 'yaw': None}, "flightTime": None}
transmitData = {"basic": {"isOn": 1, "runFlight": 1, "releaseParachute": 0}, "manualControl": {"activated": "0", "left": "0", "right": "0"}, "miscFunctions": {"beeper": "0", "lights": "0", "x": "0", "y": "0"}, "camera": {"startVid": "0", "photo": "0", "videoLength": "0"}}

app, TX_RX_main, TX_RX_sleep, Graph, mainSwitch = create_app(reciveData, transmitData) # GETS THE APP OBJ

gpsMapFunc = lambda : subprocess.call(" python graphWebsites/gpsMap_.py 1", shell=True)


startGraph = False
if __name__ == "__main__": 
    if startGraph == True:
        createGraphs(Graph, TX_RX_sleep, reciveData)


# -- STARTS & MAKES THE SWITCH THREAD
    switchThread = threading.Thread(target=mainSwitch, args=[transmitData])
    switchThread.start()
    print(f"\n ------------------------ Started Switch Thread! -------------------------")

# -- STARTS & MAKES THE GPS THREAD
    gpsThread = threading.Thread(target=gpsMapFunc)
    gpsThread.start()
    print(f"\n ------------------------ Started Gps Map! -------------------------")

# -- Starts the transmit thread
    transmitThread = threading.Thread(target=TX_RX_main, args=[app, reciveData, transmitData]) # MAKES THE TRANSMIT AND RECIVE THREAD
    time.sleep(3)
    transmitThread.start() # RUNS THE THREAD
    print(f"\n ------------------ Starthed The Transmit Thread! -------------------")
    time.sleep(0.5)


# -- Starts the main flask app
    app.run(host="0.0.0.0", debug=False, port=5000) # NOTE IF DEBUG = TRUE, THEN THE THREADS WILL BE CALLED TWICE
 




