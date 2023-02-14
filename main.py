

from website import create_app, pathToTransmitJson, readJson
#from graphs import start

import subprocess
import threading
import logging
import time
import sys
import os

from website.graphWebsites.main import start
 

app, TX_RX_main = create_app() # GETS THE APP OBJ

if __name__ == "__main__": 

    start()

    transmitThread = threading.Thread(target=TX_RX_main, args=[app]) # MAKES THE TRANSMIT AND RECIVE THREAD
    transmitThread.start() # RUNS THE THREAD

    app.run(host="0.0.0.0", debug=True, port=5000)
 







    #websiteThread = threading.Thread(target=app.run(host="0.0.0.0", port=5001, debug=debug, threaded=True)) # RUNS THE WEBSITE ON A SEPERATE THREAD (STARTS HOSTING)








