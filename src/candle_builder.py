import threading
from datetime import datetime
import pandas as pd
from helpers import CANDLE_COLS,timestamp_ms

import threading
from candle import Candle, Trade
# Ensure RAW_CANDLE_COLS is a pandas Index, Series, or appropriate type for the columns param



class CandleBuilder:
    
    
    def __init__(self, interval_sec: int,on_candle_callback):

        self.on_candle_callback = on_candle_callback
        self.interval_sec = interval_sec
        self.buffer = {"open_timestamp": None, "trades":[]}
        
        self._start_interval(None)
        
   
    def on_trade(self,raw_trade):
        new_trade = Trade.from_raw(raw_trade)
        self.buffer["trades"].append(new_trade)
        
     


    
    def _start_interval(self,prev_candle:Candle|None):

        self.buffer = {
            "prev_candle":prev_candle,
            'open_timestamp':timestamp_ms(datetime.now()),
            'trades':[]
        }

        threading.Timer(self.interval_sec,self._emit_candle)
        
        
    
    # Emits candle and restarts the interval
    def _emit_candle(self):

        if self.buffer['trades'].__len__() == 0:
            new_candle = self._create_empty_candle()

            self.on_candle_callback(new_candle)
            self._start_interval(new_candle)
            return
        

        open_timestamp = self.buffer['open_timestamp']
        close_timestamp = timestamp_ms(datetime.now())

        trades_list:list[Trade] = self.buffer['trades']

        open_price = self.buffer['prev_candle'].close_price
        close_price = trades_list[-1].price
       
        trades = pd.DataFrame(self.buffer['trades'])
        
      
        volume = trades['size'].sum();
        num_trades = trades.__len__()

        high_price = trades['price'].max()
        low_price = trades['price'].max()
        avg_price = (trades['price'] * trades['size']) / volume
        
        
        
        new_candle = Candle(open_timestamp,close_timestamp,open_price,close_price,high_price,low_price,avg_price,volume,num_trades)
        
        
    def _create_empty_candle(self):
        
        prev_candle = self.buffer['prev_candle']

        open_timestamp:int = self.buffer['open_timestamp']
        close_timestamp:int = timestamp_ms(datetime.now())

        avg_price = 0
        open_price = 0

        if prev_candle != None:
            avg_price = prev_candle.avg_price
            open_price = prev_candle.close_price

        
        return Candle(open_timestamp,close_timestamp,open_price,open_price,open_price,open_price,avg_price,0,0)
        

        
    
        

   
        
        
# interface WsTrade {
#   coin: string;
#   side: string;
#   px: string;
#   sz: string;
#   hash: string;
#   time: number;
#   // tid is 50-bit hash of (buyer_oid, seller_oid). 
#   // For a globally unique trade id, use (block_time, coin, tid)
#   tid: number;  
#   users: [string, string] // [buyer, seller]
# }