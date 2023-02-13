



from . import pathToReciveJson, pathToTransmitJson, TX_RX_sleep, logging, loggingLevel



import sqlite3
import random
import time 
import json 



"""

recive data Dict is 232 bytes


"""

def sendData():


    with open(pathToTransmitJson, "r+") as inFile: # OPENS THE TRANSMIT FILE
        jsonData = json.load(inFile) # LOADS THE FILE

    """
    EPIC SEND DATA SCIPT WIA LORA
    """
    time.sleep(random.uniform(0.3, 0.5))

    return True
        

def reciveData():
    return True # RETURNS TRUE TO NOT STOP READING AND WRITING

def elapsedTime(startTimeFloat):
    return time.time() - startTimeFloat 




def TX_RX_main():
    run , totalTime, i = True, 0, 0

    time.sleep(TX_RX_sleep/2) # SLEEPS HALF THE TIME, SO THE "sensHat.py" SCRIPT CAN WRITE FRESH DATA TO THE "transmit.json" FILE

    while True: 
        startTime = time.time() # GETS THE CURRENT TIME
        run = sendData() # TRANSMITS THE DATA, FROM THE "transmit.json" FILE

        if elapsedTime(startTime) < TX_RX_sleep * 0.6: # IF THERE IS ENOUGH TIME LEFT TO RECIVE DATA
            run = reciveData() # RECIVES THE DATA
        else:
            logging.error(f"     Didnt recive data to Cansat, because there wasnt enough time left to forfill the time constraint of {TX_RX_sleep}. Total elapsed time in this cycle: {elapsedTime(startTime)}")


        if elapsedTime(startTime) < TX_RX_sleep: # IF THERE IS ANY SPARE TIME LEFT
            time.sleep(TX_RX_sleep - elapsedTime(startTime)) # SLEEP THE SPARE TIME







        if loggingLevel <= 10: # IF YOU WANT TO LOG OUT THE RESULT
            i+=1 # ADDS 1 TO THE INDEX VARIABLE, THIS IS TO CALCULATE AVG TIME
            totalTime += elapsedTime(startTime) # ADDS THE ELAPSED TIME TO THE TOTALTIME VARIABLE
            if str(i)[len(str(i)) -1] == "8": # IF I ENDS WITH "1" (EVRY 10TH TIME)
                logging.debug(f"     Avrage Transmit and recive time: {totalTime/i}") # LOG OUT THE AVG TIME


    raise Exception("Error ending or reciving data (run=False)")





















