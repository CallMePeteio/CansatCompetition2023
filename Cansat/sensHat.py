

from . import TX_RX_sleep, logging, writeJson, loggingLevel
from . import setGlobalVarDic



from sense_hat import SenseHat
from .gpsModule import Gps
import time
import json


sense = SenseHat() # MAKES THE SENS HAT OBJECT



"""
                                                writeText

This function writes text on the rgb led matrix
The input is a list of strings that is going to be written to the led matrix, if the input is a integer then the program will sleep for the integer time

textList = This is the list of text that you want to be written on the led matrix. example: ["Pi", "Sens", 2, "HAT"]. If this is inputted the the matrix will write Pi, Sens, and then sleep for 2 seconds, then it will write HAT
textColor = This is the colour of the text written in a tuple rgb form. example: (255,255,0)
backGroundColor = This is the colour of the backgound text written in a tuple rgb form. example: (255,0,0)
scrollSpeed = This is how fast the text will scroll by, written in ineger/float form. example: 0.1

"""



def writeText(textList, textColor=(255,255,255), backGroundColor=(0,0,0), scrollSpeed=0.1): # WRITES TEXT TO THE RGB MATRIX
        for text in textList: # LOOPS OVER ALL OF THE TEXT INPUTTED

                if isinstance(text, int) == True: # CHECKS IF THE TEXT IS INTEGER
                        time.sleep(text) # SLEEP THE TIME INPUTTED
                else:
                        sense.show_message(text, text_colour=textColor, back_colour=backGroundColor, scroll_speed=scrollSpeed) # DISPLAYES THE TEXT


"""
                                                getSensorData

This function gets all of the snesor data from the raspberry pi hat,
The function returns a dictionary of all of the data: Temp, humidity, pressure and data from the accelerometer

decimalPoint = This is how mutch the function will round off the snesor data. if decimalPoint = 1 then you will get 1 decimal point: 16.1



"""

def getSensorData(decimalPoint=1):

        temp = round(sense.get_temperature(), decimalPoint) # GET STE TEMPERATURE FROM THE TEMPRATURE SENSOR
        tempPressure = round(sense.get_temperature_from_pressure(), decimalPoint) # GETS THE THE TEMPRATRUE FROM THE PRESSURE SENSOR

        humidity = round(sense.get_humidity(), decimalPoint) # GETS THE HUMIDITY
        pressure = round(sense.get_pressure(), decimalPoint) # GETS THE ATMOSPHERIC PRESSURE

        #accel = sense.get_accelerometer() # THIS IS THE ACCELERATION DATA

        accel = sense.get_accelerometer_raw() # THIS THIS IS THE
        orientation = sense.get_orientation_degrees() # GETS THE ORIENTATION OF THE SENS HAT IN DEGREES





        #return {"temprature": temp, "tempPressure": tempPressure, "humidity": humidity, "acceleration": accel} # RETURNS THE DATA IN A DICT
        #print(sense.get_compass())
        return [temp, tempPressure, humidity, pressure, accel["x"], accel["y"], accel["z"], round(orientation["roll"], decimalPoint), round(orientation["pitch"], decimalPoint), round(orientation["yaw"], decimalPoint)]






def writeSensorData(gpsData, transmitData): 

        dataDict = {"gps": {"lat": None, "lon": None}, "telemData": {"temprature": None, "tempPressure": None, "humidity": None}, "acceleration": {"x": None, "y": None, "z": None}}

        while True: 
                startTime = time.time() # GETS THE CURRENT TIME

                sensorData = getSensorData() # GETS THE DATA FROM THE PI SENS HAT (list)

                dataDict = {"gps": {"lat": gpsData[0], "lon": gpsData[1]}, "telemData": {"temprature": sensorData[0], "tempPressure": sensorData[1], "humidity": sensorData[2], "pressure": sensorData[3]}, "acceleration": {"x": sensorData[4], "y": sensorData[5], "z": sensorData[6]}, "orientation": {"roll":sensorData[7], "pitch": sensorData[8], "yaw": sensorData[9]}}
                setGlobalVarDic(dataDict, transmitData)

                elapsedTime = time.time() - startTime # CALCULATES THE ELAPSED TIME SINCE WE STARTED
                if elapsedTime < TX_RX_sleep: # IF THE SCRIPT HAS USED MORE TIME THAN IT SHULD
                        time.sleep(TX_RX_sleep - elapsedTime) # SLEEPS THE PERFECT AMOUNT OF TIME
                else: 
                        logging.critical(f"      The write sensor script used to mutch time, time constraint: {TX_RX_sleep}. Used time: {elapsedTime}")





