

from . import TX_RX_sleep, logging, writeJson, loggingLevel
from . import setGlobalVarDic


from adafruit_bitbangio import I2C as BitBangI2C
from adafruit_ccs811 import CCS811
from sense_hat import SenseHat
from .gpsModule import Gps

import adafruit_bme680
import board
import time
import json


i2c = BitBangI2C(board.SCL, board.SDA) # ININTIALIZES THE I2C CONNECTION

ccs811 = CCS811(i2c) # CONNECTS TO THE "cca811" SENSOR
time.sleep(2) # SLEEPS A BEIT TO MAKE SURE THE "ccs811" SENSOR IS DONE
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c) # ININTIALIZES THE "bme680" SENSOR

#sense = SenseHat() # MAKES THE SENS HAT OBJECT


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


def getSensorDataExternal(TX_RX_sleep, transmitData, decimalPoint=1):
        
    
    i, totalTime =0, 0
    timeout = time.time()+TX_RX_sleep+0.5 # CALCULATES THE MAXIMUM AMOUNT OF TIME THAT CAN BE USED - THE TIME IT USUALLY TAKES TO GET DATA FROM THE SENS HAT

    while time.time() < timeout: # WHILE IT HAS USED LESS TIME THAN THE TIMEOUT
        try: 
            startTime = time.time()
            if ccs811.data_ready: # IF THE SENSOR IS READY TO SEND DATA
                
 
                tvoc = ccs811.tvoc
                co2 = ccs811.eco2

                
                temp = round(bme680.temperature, decimalPoint)
                gas = round(bme680.gas, decimalPoint)
                humidity = round(bme680.humidity, decimalPoint)
                pressure = round(bme680.pressure, 3)

                #i+=1


                #elapsedTime = time.time() - startTime
                #totalTime+=elapsedTime
                #logging.critical(f"    Total Time: {totalTime}") 
                #logging.critical(f"    Avrage Time: {totalTime/i}")
                
                if tvoc > 2000: # ADDS A FILTER SO WE DONT GET CRAZY HIGHT RESULTS, THAT SOMETIMES HAPPENDS
                    tvoc = trnasmitData["telemData"]["tvoc"]
                
                return [temp, pressure, humidity, gas, co2, tvoc]
            else:
                pass
                #elapsedTime = time.time() - startTime
                #totalTime+=elapsedTime
                
            
                #i+=1
                time.sleep(i/5)
                #if i > 0:
                #    logging.critical(f"    Total Time: {totalTime}") 
                #    logging.critical(f"    Avrage time: {totalTime/i} ")
        except Exception as error:
            logging.error(f"     There was an error reading data from the external Sensors \nError msg:     {error}")
            time.sleep(TX_RX_sleep/4)
    
    logging.critical("      External data reading took to long to read!")
    return None




def writeSensorData(gpsData, transmitData): 
    i, totalTime =0, 0
    dataDict = {"gps": {"lat": None, "lon": None}, "telemData": {"temprature": None, "pressure": None, "humidity": None, "gas": None, "co2": None, "tvoc": None}}
    while True: 
            startTime = time.time() # GETS THE CURRENT TIME

                #sensorData = getSensorData() # GETS THE DATA FROM THE PI SENS HAT (list)
                #print(sensorData)

            exSensData = getSensorDataExternal(TX_RX_sleep, transmitData)
            #exSensData = None
            if exSensData != None:     
                dataDict = {"gps": {"lat": gpsData[0], "lon": gpsData[1]}, "telemData": {"temprature": exSensData[0], "pressure": exSensData[1], "humidity": exSensData[2], "gas": exSensData[3], "co2": exSensData[4], "tvoc": exSensData[5]}}
                setGlobalVarDic(dataDict, transmitData)

                #dataDict = {"gps": {"lat": gpsData[0], "lon": gpsData[1]}, "telemData": {"temprature": sensorData[0], "tempPressure": sensorData[1], "humidity": sensorData[2], "pressure": sensorData[3]}, "acceleration": {"x": sensorData[4], "y": sensorData[5], "z": sensorData[6]}, "orientation": {"roll":sensorData[7], "pitch": sensorData[8], "yaw": sensorData[9]}}
                #setGlobalVarDic(dataDict, transmitData)

                elapsedTime = time.time() - startTime # CALCULATES THE ELAPSED TIME SINCE WE STARTED
                if elapsedTime < TX_RX_sleep: # IF THE SCRIPT HAS USED MORE TIME THAN IT SHULD
                        time.sleep(TX_RX_sleep - elapsedTime) # SLEEPS THE PERFECT AMOUNT OF TIME
                
                #else: 
                        #logging.critical(f"      The write sensor script used to mutch time, time constraint: {TX_RX_sleep}. Used time: {elapsedTime}")
                
                if loggingLevel >= 10:
                    i+=1
                    totalTime += time.time() - startTime

                    if str(i)[len(str(i))-1] == "8":
                        logging.info(f"     Avrage sensor upate time: {totalTime/i}")


#while True: 
    #data = getSensorDataExternal()
    #print(data)


    #time.sleep(0.5)




#writeSensorData(1, 2)


