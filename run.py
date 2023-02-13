





from Cansat import startApp
import threading

if __name__ == "__main__": 
    writeSensorData, TX_RX_main, action = startApp()

# -- STARTS & MAKES THE TEMPERATURE THREAD
    sensThread = threading.Thread(target=writeSensorData)
    sensThread.start()
    print(f"\n ---------------- Started The Sens Hat Sensors! ----------------")


# -- STARTS THE SEND AND WRITE DATA SCRIPT
    TX_RX_Thread = threading.Thread(target=TX_RX_main)
    TX_RX_Thread.start()
    print(f"\n ---------------- Started The TX RX Script! ----------------")

# -- STARTS THE SEND AND WRITE DATA SCRIPT
    TX_RX_Thread = threading.Thread(target=action)
    TX_RX_Thread.start()
    print(f"\n ---------------- Started The Action Script! ----------------")










