import threading
import time


def createGraphs(Graph, TX_RX_sleep, reciveData): 


#   {
#       "graph_key": [
#           ["db_column_1", "db_column_2"],
#           ["data_dict_key", ["data_key"], "time_key"],
#           port_number
#       ],
#       ...
#   }
#
#   graph_key: A string representing the type of telemetry data for the graph (e.g., "temperature", "humidity", "pressure").
#   db_column_1 and db_column_2: Strings representing the column names in the database that will be used as the x and y axes of the graph, respectively.
#   data_dict_key: A string representing the key in the reciveData dictionary that contains the telemetry data.
#   data_key: A list containing a single string representing the key within the reciveData[data_dict_key] dictionary that contains the y-axis data for the graph.
#   time_key: A string representing the key within the reciveData dictionary that contains the x-axis data (time) for the graph.
#   port_number: An integer representing the port number on which the graph's web server will run.


# -- THIS KEEPS TRACK OF THE PORT AND IP ADRESS OF THE 
    grafHostDict = {"temperature": [["flightTime", "temperature"], ["telemData", ["temprature"], "flightTime"], 5200], 
                    "pressure": [["flightTime", "pressure"], ["telemData", ["pressure"], "flightTime"], 5100], 
                    "humidity": [["flightTime", "humidity"], ["telemData", ["humidity"], "flightTime"], 5300],  
                    "gas": [["flightTime", "gas"], ["telemData", ["gas"], "flightTime"], 5400], 
                    "co2": [["flightTime", "co2"], ["telemData", ["co2"], "flightTime"], 5600], 
                    "tvoc": [["flightTime", "tvoc"], ["telemData", ["tvoc"], "flightTime"], 5700], 
                    } 

    sleepMultiplier = 2 # HOW LONG IT WILL TAKE FOR THE DIFFRENT GRAPHS TO START UP   
    graphList = []

# -- MAKES THE GRAPH OBJECTS
    #temperaturePressureGraph = Graph(grafHostDict["tempPressure"][0], grafHostDict["tempPressure"][1], TX_RX_sleep, grafHostDict["tempPressure"][2])
    temperatureGraph = Graph(grafHostDict["temperature"][0], grafHostDict["temperature"][1], TX_RX_sleep, grafHostDict["temperature"][2])
    graphList.append(temperatureGraph)

    pressureGraph = Graph(grafHostDict["pressure"][0], grafHostDict["pressure"][1], TX_RX_sleep, grafHostDict["pressure"][2])
    graphList.append(pressureGraph)

    humidityGraph = Graph(grafHostDict["humidity"][0], grafHostDict["humidity"][1], TX_RX_sleep, grafHostDict["humidity"][2])
    graphList.append(humidityGraph)

    gasGraph = Graph(grafHostDict["gas"][0], grafHostDict["gas"][1], TX_RX_sleep, grafHostDict["gas"][2])
    graphList.append(gasGraph)

    co2Graph = Graph(grafHostDict["co2"][0], grafHostDict["co2"][1], TX_RX_sleep, grafHostDict["co2"][2])
    graphList.append(co2Graph)

    tvocGraph = Graph(grafHostDict["tvoc"][0], grafHostDict["tvoc"][1], TX_RX_sleep, grafHostDict["tvoc"][2])
    graphList.append(tvocGraph)


    for graph in graphList: 
        graphThread = threading.Thread(target=graph.start, args=[reciveData]) 
        graphThread.start()
        time.sleep(TX_RX_sleep*sleepMultiplier)







"""
# -- STARTS & MAKES THE TEMPERATURE THREAD
    tempThread = threading.Thread(target=temperatureGraph.start, args=[reciveData])
    tempThread.start()
    time.sleep(TX_RX_sleep*sleepMultiplier)

# -- STARTS & MAKES THE PRESSURE THREAD
    pressureThread = threading.Thread(target=pressureGraph.start, args=[reciveData])
    pressureThread.start()
    time.sleep(TX_RX_sleep*sleepMultiplier)

# -- STARTS & MAKES THE HUMIDITY THREAD
    humidityThread = threading.Thread(target=humidityGraph.start, args=[reciveData])
    humidityThread.start()
    time.sleep(TX_RX_sleep*sleepMultiplier)

# -- STARTS & MAKES THE PRESSURE THREAD
    tempPressureThread = threading.Thread(target=gasGraph.start, args=[reciveData])
    tempPressureThread.start()
    time.sleep(TX_RX_sleep*sleepMultiplier)

# -- STARTS & MAKES THE PRESSURE THREAD
    tempPressureThread = threading.Thread(target=gasGraph.start, args=[reciveData])
    tempPressureThread.start()
    time.sleep(TX_RX_sleep*sleepMultiplier)


"""