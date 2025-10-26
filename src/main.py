import datetime
import tkinter
import pandas as pd
import numpy as np
from hyperliquid.info import Info
from hyperliquid.utils import constants
from plot import plot
from dex import Dex
from time_interval import TimeInterval
import time
def main():
    
    dex = Dex()
    start = datetime.datetime.now().replace(hour=7)
    
    # Option 1: Standard minute candles (API supports 1m minimum)
    # dex.subscribe("ETH",TimeInterval.MINUTE_1,start,print)
    
    # Option 2: Sub-minute candles using trades (supports any interval)
    # Examples: 1 second, 15 seconds, 30 seconds, etc.
    dex.subscribe_subminute("ETH", 15, callbackprint)
    
    # Keep the program running to receive real-time updates
 
    while True:
        time.sleep(1)

    
    
    
    # window = tkinter.Tk()
    # window.title("DMSO Terminal")
    # window.geometry("1000x1000")

    # plot(window, df)

    # window.mainloop()





if __name__ == "__main__":
    main()