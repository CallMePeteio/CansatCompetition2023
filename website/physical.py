


from . import TX_RX_sleep


import RPi.GPIO as gpio

import time



switchDict = {"switch1": [17, 0], "switch2": [27, 0], "manualDrive": [22, 0]}

# Set GPIO mode to BCM
gpio.setmode(gpio.BCM)

# Set GPIO pin to input mode


for key, value in switchDict.items():
    gpio.setup(value[0], gpio.IN)





def mainSwitch(transmitData): 

    while True:

        for switches in switchDict.keys():

            if gpio.input(switchDict[switches][0]) == True and switchDict[switches][1] == 0:
                switchDict[switches][1] = 1
                print(f"{switches} ON")

            elif gpio.input(switchDict[switches][0]) == False and switchDict[switches][1] == 1: 
                switchDict[switches][1] = 0
                print(f"{switches} OFF")



            

        #if gpio.input(switchDict["switch2"][0]):
        #    print("switch2")
        #if gpio.input(switchDict["manualDrive"][0]):
        #    print("manualDrive")



        time.sleep(TX_RX_sleep*2)

