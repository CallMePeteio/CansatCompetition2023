



import threading
import logging
import time

"""
Level: NOTSET > DEBUG > INFO > WARNING > ERROR > CRITICAL
Value:   0    >  10   >  20  >    30   >  40   >  50
"""
loggingLevel = 10 # DEFINES THE LOGGING LEVEL
logger = logging.getLogger() # MAKES THE LOGGING OBJECT
logger.setLevel(loggingLevel) # SETS THE LEVEL AS DEFINED ABOVE

pathToReciveJson = "/home/pi/Desktop/coding/Cansat/instance/recive.json" # RECIVE JSON FULL PATH
pathToTransmitJson = "/home/pi/Desktop/coding/Cansat/instance/transmit.json" # TRANSMIT JSON FULL PATH

videoPath="/home/pi/Desktop/coding/Cansat/video/"
imgPath="/home/pi/Desktop/coding/Cansat/img/"
videoRes, fps, imgScaleXY, imgFlip = (640, 480), 10, (1,1), -1

TX_RX_sleep = 1






def startApp(): 
    from .camera import Camera

    from .sensHat import writeSensorData
    from .writeData import TX_RX_main
    from .recive import action

    return writeSensorData, TX_RX_main, action

