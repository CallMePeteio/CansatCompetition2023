





from Cansat import startApp
import threading

gpsData = [67.206836, 15.15958, '2023-18-2 12:0:9', 10, 14.4, 0.41, 161.29, 1.22]

transmitData = {'gps': {'lat': 67.206836, 'lon': 15.15958}, 'telemData': {'temprature': 41.8, 'tempPressure': 41.3, 'humidity': 20.3, 'pressure': 1003.7}, 'acceleration': {'x': -0.05850004777312279, 'y': 0.14397600293159485, 'z': 0.9679639339447021}, 'orientation': {'roll': 26.0, 'pitch': 6.8, 'yaw': 126.3}}
reciveData = {"basic": {"isOn": "1", "prime": "1", "reset": "0"}, "manualControl": {"activated": "0", "left": "0", "right": "0"}, "miscFunctions": {"beeper": "0", "lights": "0", "x": "0", "y": "0"}, "camera": {"startVid": "0", "photo": "0", "videoLength": ""}}


if __name__ == "__main__": 
    writeSensorData, TX_RX_main, getGpsPos, action = startApp()

# -- STARTS & MAKES THE SENS HAT THREAD
    sensThread = threading.Thread(target=writeSensorData, args=(gpsData, transmitData))
    sensThread.start()
    print(f"\n ---------------- Started The Sens Hat Sensors! ----------------")    

# -- STARTS & MAKES THE SENS HAT THREAD
    gpsThread = threading.Thread(target=getGpsPos, args=(gpsData,))
    gpsThread.start()
    print(f"\n ---------------- Started The Sens Hat Sensors! ----------------")

# -- STARTS THE SEND AND WRITE DATA SCRIPT
    TX_RX_Thread = threading.Thread(target=TX_RX_main, args=(gpsData, transmitData, reciveData))
    TX_RX_Thread.start()
    print(f"\n ---------------- Started The TX RX Script! ----------------")

# -- STARTS THE SEND AND WRITE DATA SCRIPT
    actionThread = threading.Thread(target=action, args=(reciveData, ))
    actionThread.start()
    print(f"\n ---------------- Started The Action Script! ---------------- \n")










