





from Cansat import startApp
import threading

gpsData = [67.206836, 15.15958, '2023-18-2 12:0:9', 10, 14.4, 0.41, 161.29, 1.22]


if __name__ == "__main__": 
    writeSensorData, TX_RX_main, getGpsPos, action = startApp()

# -- STARTS & MAKES THE SENS HAT THREAD
    sensThread = threading.Thread(target=writeSensorData, args=(gpsData,))
    sensThread.start()
    print(f"\n ---------------- Started The Sens Hat Sensors! ----------------")    

# -- STARTS & MAKES THE SENS HAT THREAD
    gpsThread = threading.Thread(target=getGpsPos, args=(gpsData,))
    gpsThread.start()
    print(f"\n ---------------- Started The Sens Hat Sensors! ----------------")

# -- STARTS THE SEND AND WRITE DATA SCRIPT
    TX_RX_Thread = threading.Thread(target=TX_RX_main, args=[gpsData, ])
    TX_RX_Thread.start()
    print(f"\n ---------------- Started The TX RX Script! ----------------")

# -- STARTS THE SEND AND WRITE DATA SCRIPT
    actionThread = threading.Thread(target=action)
    actionThread.start()
    print(f"\n ---------------- Started The Action Script! ---------------- \n")










