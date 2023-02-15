

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
pressureFunc = lambda : subprocess.call(" python graphWebsites/pressure.py 1", shell=True)
gpsMapFunc = lambda : subprocess.call(" python graphWebsites/gpsMap_.py 1", shell=True)

if __name__ == "__main__": 


# -- STARTS & MAKES THE TEMPERATURE THREAD
    tempThread = threading.Thread(target=tempFunc)
    tempThread.start()
    print(f"\n -------------- Started The Temperature Graph! ---------------")

# -- STARTS & MAKES THE PRESSURE THREAD
    pressureThread = threading.Thread(target=pressureFunc)
    pressureThread.start()
    print(f"\n ---------------- Started The Pressure Graph! ----------------")

# -- STARTS & MAKES THE GPS THREAD
    gpsThread = threading.Thread(target=gpsMapFunc)
    gpsThread.start()
    print(f"\n ------------------------ Started Gps Map! -------------------------")

# -- Starts the transmit thread
    transmitThread = threading.Thread(target=TX_RX_main, args=[app]) # MAKES THE TRANSMIT AND RECIVE THREAD
    transmitThread.start() # RUNS THE THREAD
    print(f"\n ------------------ Starthed The Transmit Thread! -------------------")


# -- Starts the main flask app
    app.run(host="0.0.0.0", debug=True, port=5000)
 







    #websiteThread = threading.Thread(target=app.run(host="0.0.0.0", port=5001, debug=debug, threaded=True)) # RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)








