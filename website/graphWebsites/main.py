


import subprocess
import threading
import time
import os 



tempFunc = lambda : subprocess.call(" python website/graphWebsites/graphs/temperature.py 1", shell=True)
pressureFunc = lambda : subprocess.call(" python website/graphWebsites/graphs/pressure.py 1", shell=True)
gpsMapFunc = lambda : subprocess.call(" python website/graphWebsites/graphs/gpsMap.py 1", shell=True)

def start():

# -- STARTS & MAKES THE TEMPERATURE THREAD
    tempThread = threading.Thread(target=tempFunc)
    tempThread.start()
    print(f"\n \n \n ---------------- Started The Temperature Graph! ----------------")

# -- STARTS & MAKES THE PRESSURE THREAD
    pressureThread = threading.Thread(target=pressureFunc)
    pressureThread.start()
    print(f"\n \n \n ---------------- Started The Pressure Graph! ----------------")

# -- STARTS & MAKES THE GPS THREAD
    gpsThread = threading.Thread(target=gpsMapFunc)
    gpsThread.start()
    print(f"\n \n \n ---------------- Started Gps Map! ----------------")


start()

