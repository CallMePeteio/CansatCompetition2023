
import sys
import os

from website import create_app, pathToTransmitJson, readJson
#from graphs import start

import subprocess
import threading
import logging
import time
import sys
import os

#from website.graphWebsites.main import start


app, TX_RX_main, TX_RX_sleep, Graph = create_app() # GETS THE APP OBJ


reciveData = {'gps': {'lat': 67.206836, 'lon': 15.15958}, 'telemData': {'temprature': None, 'tempPressure': None, 'humidity': None, 'pressure': 1003.7}, 'acceleration': {'x': -0.05850004777312279, 'y': 0.14397600293159485, 'z': 0.9679639339447021}, 'orientation': {'roll': 26.0, 'pitch': 6.8, 'yaw': 126.3}, "flightTime": None}


# THIS KEEPS TRACK OF THE PORT AND IP ADRESS OF THE 
grafHostDict = {"temperature": [["flightTime", "temperature"], ["telemData", ["temprature"], "flightTime"], 5200], 
                "tempPressure": [["flightTime", "temperature"], ["telemData", ["tempPressure"], "flightTime"], 5100], 
                "humidity": [["flightTime", "humidity"], ["telemData", ["humidity"], "flightTime"], 5300],  
                "pressure": [["flightTime", "pressure"], ["telemData", ["pressure"], "flightTime"], 5400], 
                } 

temperaturePressureGraph = Graph(grafHostDict["tempPressure"][0], grafHostDict["tempPressure"][1], TX_RX_sleep, grafHostDict["tempPressure"][2])
temperatureGraph = Graph(grafHostDict["temperature"][0], grafHostDict["temperature"][1], TX_RX_sleep, grafHostDict["temperature"][2])
humidityGraph = Graph(grafHostDict["humidity"][0], grafHostDict["humidity"][1], TX_RX_sleep, grafHostDict["humidity"][2])
pressureGraph = Graph(grafHostDict["pressure"][0], grafHostDict["pressure"][1], TX_RX_sleep, grafHostDict["pressure"][2])



#
#tempPressure = lambda : subprocess.call(" python graphWebsites/tempPressure.py 1", shell=True)
gpsMapFunc = lambda : subprocess.call(" python graphWebsites/gpsMap_.py 1", shell=True)
#humidityFunc = lambda : subprocess.call(" python graphWebsites/humidity.py 1", shell=True)
#pressureFunc = lambda : subprocess.call(" python graphWebsites/pressure.py 1", shell=True)
#orientationFunc = lambda : subprocess.call(" python graphWebsites/orientation.py 1", shell=True)


startGraph = True

if __name__ == "__main__": 

    if startGraph == True:
    # -- STARTS & MAKES THE TEMPERATURE THREAD
        tempThread = threading.Thread(target=temperatureGraph.start, args=[reciveData])
        tempThread.start()
        time.sleep(TX_RX_sleep)

    # -- STARTS & MAKES THE PRESSURE THREAD
        tempPressureThread = threading.Thread(target=temperaturePressureGraph.start, args=[reciveData])
        tempPressureThread.start()
        time.sleep(TX_RX_sleep)

    # -- STARTS & MAKES THE HUMIDITY THREAD
        humidityThread = threading.Thread(target=humidityGraph.start, args=[reciveData])
        humidityThread.start()
        time.sleep(TX_RX_sleep)

    # -- STARTS & MAKES THE PRESSURE THREAD
        pressureThread = threading.Thread(target=pressureGraph.start, args=[reciveData])
        pressureThread.start()
        time.sleep(TX_RX_sleep*2)

        
    # -- STARTS & MAKES THE Orientation THREAD
        #orientationThread = threading.Thread(target=orientationFunc)
        #orientationThread.start()
        #print(f"\n ------------------------ Started Orientation Graph! -------------------------")




# -- STARTS & MAKES THE GPS THREAD
    gpsThread = threading.Thread(target=gpsMapFunc)
    gpsThread.start()
    print(f"\n ------------------------ Started Gps Map! -------------------------")

# -- Starts the transmit thread
    transmitThread = threading.Thread(target=TX_RX_main, args=[app, reciveData]) # MAKES THE TRANSMIT AND RECIVE THREAD
    time.sleep(3)
    transmitThread.start() # RUNS THE THREAD
    print(f"\n ------------------ Starthed The Transmit Thread! -------------------")
    time.sleep(0.5)


# -- Starts the main flask app
    app.run(host="0.0.0.0", debug=False, port=5000) # NOTE IF DEBUG = TRUE, THEN THE THREADS WILL BE CALLED TWICE
 







    #websiteThread = threading.Thread(target=app.run(host="0.0.0.0", port=5001, debug=debug, threaded=True)) # RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)








