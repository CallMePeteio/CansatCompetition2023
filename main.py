

from website import create_app, pathToTransmitJson, readJson
#from graphs import start

import subprocess
import threading
import logging
import time
import sys
import os

#from website.graphWebsites.main import start
 

app, TX_RX_main = create_app() # GETS THE APP OBJ

tempFunc = lambda : subprocess.call(" python graphWebsites/temperature.py 1", shell=True)
tempPressure = lambda : subprocess.call(" python graphWebsites/tempPressure.py 1", shell=True)
gpsMapFunc = lambda : subprocess.call(" python graphWebsites/gpsMap_.py 1", shell=True)
humidityFunc = lambda : subprocess.call(" python graphWebsites/humidity.py 1", shell=True)

if __name__ == "__main__": 


# -- STARTS & MAKES THE TEMPERATURE THREAD
    tempThread = threading.Thread(target=tempFunc)
    tempThread.start()
    print(f"\n -------------- Started The Temperature Graph! ---------------")

# -- STARTS & MAKES THE PRESSURE THREAD
    tempPressureThread = threading.Thread(target=tempPressure)
    tempPressureThread.start()
    print(f"\n ---------------- Started The Pressure Graph! ----------------")

# -- STARTS & MAKES THE HUMIDITY THREAD
    humidityThread = threading.Thread(target=humidityFunc)
    humidityThread.start()
    print(f"\n ------------------------ Started Humidity Graph! -------------------------")

# -- STARTS & MAKES THE GPS THREAD
    gpsThread = threading.Thread(target=gpsMapFunc)
    gpsThread.start()
    print(f"\n ------------------------ Started Gps Map! -------------------------")

# -- Starts the transmit thread
    transmitThread = threading.Thread(target=TX_RX_main, args=[app]) # MAKES THE TRANSMIT AND RECIVE THREAD
    time.sleep(3)
    transmitThread.start() # RUNS THE THREAD
    print(f"\n ------------------ Starthed The Transmit Thread! -------------------")
    time.sleep(0.5)


# -- Starts the main flask app
    app.run(host="0.0.0.0", debug=False, port=5000) # NOTE IF DEBUG = TRUE, THEN THE THREADS WILL BE CALLED TWICE
 







    #websiteThread = threading.Thread(target=app.run(host="0.0.0.0", port=5001, debug=debug, threaded=True)) # RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)








