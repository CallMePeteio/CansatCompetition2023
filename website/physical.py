
from flask import current_app

from . import writeGobalFlaskVar
from . import readGobalFlaskVar
from . import loggingLevel
from . import TX_RX_sleep
from . import dataLock
from . import logging

import RPi.GPIO as gpio 
import time 
import sys
import os




sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add the parent directory of the current file to the sys.path list
from libaries.ADClibary import ADS1115 # import the ADS1115 Class

ads1115 = ADS1115() # GETS THE OBJECT
ADS1115_REG_CONFIG_PGA_6_144V = 0x00 # 6.144V range = Gain 2/3
ads1115.set_addr_ADS1115(0x48) # SETS THE ADRESS OF THE ADC CONVERTED
ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V) # Sets the gain and input voltage range.



switchDict = {"switch1": [17, 0], "switch2": [27, 0], "manualDrive": [26, 0]}  # SWITCH DICTIONARY WITH GPIO PIN NUMBERS AND STATES
gpio.setmode(gpio.BCM)  # SETS GPIO PIN NUMBERING MODE TO BCM
for key, value in switchDict.items():  # SETS UP GPIO PINS FOR INPUT
    gpio.setup(value[0], gpio.IN)





# _________________________________ mainSwitch __________________________________
# Monitors the status of physical switches and updates switchDict accordingly.
# transmitData: Ununsed variable (to be implemented in future updates)
def mainSwitch(app, transmitData): 
    voltageRange, i, prevServoDeg = [70, 3850], 0, None # THIS KEEPS TRACK OF THE MAX AND MINIMUM VOLTAGE LEVELS GOTTEN FROM THE ADC CONVERTER.

    with app.app_context(): # TO GET FULL PERMISSIONS TO READ AND WRITE TO DB, AND GLOBAL VARIABLES
        while True:


            for switches in switchDict.keys():
                # CHECKS IF SWITCH IS TURNED ON AND UPDATES STATE TO 1
                if gpio.input(switchDict[switches][0]) == True and switchDict[switches][1] == 0:
                    switchDict[switches][1] = 1
                    logging.info(f"     {switches} Turned ON")


                    if switches == "manualDrive":
                        writeGobalFlaskVar(["transmitData", "manualControl", "activated"], "1", dataLock, True)


                # CHECKS IF SWITCH IS TURNED OFF AND UPDATES STATE TO 0
                elif gpio.input(switchDict[switches][0]) == False and switchDict[switches][1] == 1: 
                    switchDict[switches][1] = 0
                    logging.info(f"     {switches} Turned OFF")

                    if switches == "manualDrive":
                        writeGobalFlaskVar(["transmitData", "manualControl", "activated"], "0", dataLock, True)






            if switchDict["manualDrive"][1] == 1: # CHECKS IF THE "manualDrive" SWITCH IS TURNED ON
                a0 = ads1115.read_voltage(0)["r"] # READS THE VOLTAGE OVER THE POTENTIOMENTER, IN MILIVOLTS
                voltageRange = checkVoltageRange(voltageRange, a0) # SETS THE MAX AND MINIMUM VOLTAGE RANGE, THIS IS FOR MORE ACCURATE CALCULATING.

                if  a0 > 2250 and a0 < 2900: # THIS IS SOME PADDING TO MAKE IT EASYER TO TURN IT STRAIGHT
                    servoDeg = 90 # SETS THE SERVO IN THE MIDDLE  
                else: 
                    servoDeg = convertNum(voltageRange, 180, a0) # CONVERTS THE VOLTAGE FROM 68-3900 TO DEGREES FROM 0 AND 90

                intServoDeg = int(round(servoDeg, 0))
                if intServoDeg != prevServoDeg and intServoDeg +1 != prevServoDeg and intServoDeg -1 != prevServoDeg and intServoDeg +2 != prevServoDeg and intServoDeg -2 != prevServoDeg and intServoDeg +3 != prevServoDeg and intServoDeg -3 != prevServoDeg:  # CHECKS IF THE POSITION HAS CHANGED SINCE LAST TIME
                    writeGobalFlaskVar(["transmitData", "manualControl", "degrees"], str(servoDeg), dataLock, False) # CHANGES THE GLOBAL FLASK VARIABLE, THAT CONTAINS THE INFORTMATION ON WHAT POSITION THE SERVO SHULD DO
                    prevServoDeg = intServoDeg
                    
                




                if loggingLevel <= 10: # IF IT SHULD LOG OUT THE CURRENT HEADING
                    i+=1 # ADDS 1 TO I, TO NOT PRINT OUT ALL OF THE TIME
                    if str(i)[len(str(i)) -1] == "8" and prevServoDeg != None: # IF I END WITH 8 (EVRY 10'TH TIME), AND "servoDeg" IS DEFINED
                        logging.debug(f"     Current Servo Pos: {prevServoDeg}") # LOG OUT THE CURRENT HEADING

            time.sleep(TX_RX_sleep)  # SLEEP 


def returnNewDict(path, value, globalDic):
    newData = globalDic
    newData[path[0]][path[1]] = value
    return newData

def convertNum(numRange, outputMax, number): # CONVERTS NUMBER TO ANOTHER NUMBER
    outputNum = (number - numRange[0]) / (numRange[1] - numRange[0]) * outputMax
    return round(outputNum, 1)

def checkVoltageRange(voltageRange, currentVoltage): 
    if currentVoltage < voltageRange[0]:
        return [currentVoltage, voltageRange[1]]
    elif currentVoltage > voltageRange[1]:
        return [voltageRange[0], currentVoltage]
    return voltageRange