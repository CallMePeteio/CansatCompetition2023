

from . import pathToTransmitJson, pathToReciveJson, TX_RX_sleep, logging, writeJson, loggingLevel, pathToBackEndJson



from sense_hat import SenseHat
from .gpsModule import Gps
import time
import json


sense = SenseHat() # MAKES THE SENS HAT OBJECT


#sense.show_message("HELLO ROBIN", text_colour=(255,0,0), back_colour=(0,255,0), scroll_speed=0.05) # DISPLAYES A MESSAGE
#sense.clear((255,255,255)) # DISPLAYES A COLOUR ON THE RGB SCREEN


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
        pressure = round(sense.get_pressure(), decimalPoint) # GETS THE PRESSURE DATA FROM THE SENS HAT, ROUNDS OFF THE RESULT

        temp = round(sense.get_temperature(), decimalPoint) # GET STE TEMPERATURE FROM THE TEMPRATURE SENSOR
        tempPressure = round(sense.get_temperature_from_pressure(), decimalPoint) # GETS THE THE TEMPRATRUE FROM THE PRESSURE SENSOR

        humidity = round(sense.get_humidity(), decimalPoint) # GETS THE HUMIDITY

        #accel = sense.get_accelerometer() # THIS IS THE ACCELERATION DATA
        accel = sense.get_accelerometer_raw() # THIS THIS IS THE

        #return {"temprature": temp, "tempPressure": tempPressure, "humidity": humidity, "acceleration": accel} # RETURNS THE DATA IN A DICT
        return [temp, tempPressure, humidity, accel["x"], accel["y"], accel["z"]]




def writeSensorData(gpsData): 

        dataDict = {"gps": {"lat": None, "lon": None}, "telemData": {"temprature": None, "tempPressure": None, "humidity": None}, "acceleration": {"x": None, "y": None, "z": None}}

        while True: 
                startTime = time.time() # GETS THE CURRENT TIME
                data = getSensorData() # GETS THE SENSOR DATA


                with open(pathToTransmitJson, "w") as outFile: # OPENS THE TRANSMIT FILE
                        sensorData = getSensorData() # GETS THE DATA FROM THE PI SENS HAT (list)
                        dataDict = {"gps": {"lat": gpsData[0], "lon": gpsData[1]}, "telemData": {"temprature": sensorData[0], "tempPressure": sensorData[1], "humidity": sensorData[2]}, "acceleration": {"x": sensorData[3], "y": sensorData[4], "z": sensorData[5]}}
                        jsonData = json.dump(dataDict, outFile) # OWERWRITES THE DATA IN THE JSON FILE, WITH THE NEW DATA GETHERED



                elapsedTime = time.time() - startTime # CALCULATES THE ELAPSED TIME SINCE WE STARTED
                if elapsedTime < TX_RX_sleep: # IF THE SCRIPT HAS USED MORE TIME THAN IT SHULD
                        time.sleep(TX_RX_sleep - elapsedTime) # SLEEPS THE PERFECT AMOUNT OF TIME
                else: 
                        logging.critical(f"      The write sensor script used to mutch time, time constraint: {TX_RX_sleep}. Used time: {elapsedTime}")










#while True: 
#    textList = ["PEPSI POWER"]
#    writeText(textList=textList, textColor=(0, 71, 171), scrollSpeed=0.15)


#while True:
#
#        print()
#        print(getSensorData())
#        time.sleep(0.1)

