import threading
import time


def createGraphs(Graph, TX_RX_sleep, reciveData): 

# -- THIS KEEPS TRACK OF THE PORT AND IP ADRESS OF THE 
    grafHostDict = {"temperature": [["flightTime", "temperature"], ["telemData", ["temprature"], "flightTime"], 5200], 
                    "tempPressure": [["flightTime", "temperature"], ["telemData", ["tempPressure"], "flightTime"], 5100], 
                    "humidity": [["flightTime", "humidity"], ["telemData", ["humidity"], "flightTime"], 5300],  
                    "pressure": [["flightTime", "pressure"], ["telemData", ["pressure"], "flightTime"], 5400], 
                    } 

# -- MAKES THE GRAPH OBJECTS
    temperaturePressureGraph = Graph(grafHostDict["tempPressure"][0], grafHostDict["tempPressure"][1], TX_RX_sleep, grafHostDict["tempPressure"][2])
    temperatureGraph = Graph(grafHostDict["temperature"][0], grafHostDict["temperature"][1], TX_RX_sleep, grafHostDict["temperature"][2])
    humidityGraph = Graph(grafHostDict["humidity"][0], grafHostDict["humidity"][1], TX_RX_sleep, grafHostDict["humidity"][2])
    pressureGraph = Graph(grafHostDict["pressure"][0], grafHostDict["pressure"][1], TX_RX_sleep, grafHostDict["pressure"][2])



# -- STARTS & MAKES THE TEMPERATURE THREAD
    tempThread = threading.Thread(target=temperatureGraph.start, args=[reciveData])
    tempThread.start()
    time.sleep(TX_RX_sleep*2)

# -- STARTS & MAKES THE PRESSURE THREAD
    tempPressureThread = threading.Thread(target=temperaturePressureGraph.start, args=[reciveData])
    tempPressureThread.start()
    time.sleep(TX_RX_sleep*2)

# -- STARTS & MAKES THE HUMIDITY THREAD
    humidityThread = threading.Thread(target=humidityGraph.start, args=[reciveData])
    humidityThread.start()
    time.sleep(TX_RX_sleep*2)

# -- STARTS & MAKES THE PRESSURE THREAD
    pressureThread = threading.Thread(target=pressureGraph.start, args=[reciveData])
    pressureThread.start()
    time.sleep(TX_RX_sleep*4)