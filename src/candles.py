import threading
from datetime import datetime
from typing import Callable
import pandas as pd
from helpers import CANDLE_COLS,timestamp_ms

import threading
from candle import Candle, Trade
# Ensure RAW_CANDLE_COLS is a pandas Index, Series, or appropriate type for the columns param



class Candles:
    
    
    def __init__(self, interval_sec: int,on_candle_callback:Callable[[pd.DataFrame], None]):

        self.dataframe = pd.DataFrame()
        self._on_candle_callback = on_candle_callback
        self.interval_sec = interval_sec
        self._buffer = {"open_timestamp": None, "trades":[]}

        self._start_interval(None)
        
   
    def on_trade(self,raw_trade):
        new_trade = Trade.from_raw(raw_trade)
        self._buffer["trades"].append(new_trade)
        
    
    
    def _start_interval(self,prev_candle:Candle|None):

        self._buffer = {
            "prev_candle":prev_candle,
            'open_timestamp':timestamp_ms(datetime.now()),
            'trades':[]
        }

        timer = threading.Timer(self.interval_sec, self._add_candle)
        timer.start()
        
  
    def _add_candle(self):

        def append_and_complete(new_candle:Candle):
            self.dataframe = pd.concat([self.dataframe, new_candle.to_dataframe()], ignore_index=True)
            self._on_candle_callback(self.dataframe)
            self._start_interval(new_candle)
    
        if self._buffer['trades'].__len__() == 0:
            append_and_complete(self._create_empty_candle())
            return
        

        open_timestamp = self._buffer['open_timestamp']
        close_timestamp = timestamp_ms(datetime.now())

        prev_candle = self._buffer['prev_candle']
        open_price = prev_candle.close_price if prev_candle != None else self._buffer['trades'][0].price
        close_price = self._buffer['trades'][-1].price
       
        trades = pd.DataFrame([{'price': t.price, 'size': t.size} for t in self._buffer['trades']])

        volume = trades['size'].sum()
        num_trades = trades.__len__()
        high_price = trades['price'].max()
        low_price = trades['price'].min()  # Fixed: was .max()
        avg_price = (trades['price'] * trades['size']).sum() / volume  # Fixed: sum before divide
        
        new_candle = Candle(open_timestamp,close_timestamp,open_price,close_price,high_price,low_price,avg_price,volume,num_trades)
        append_and_complete(new_candle)
        
    def _create_empty_candle(self):
        
        prev_candle = self._buffer['prev_candle']

        open_timestamp:int = self._buffer['open_timestamp']
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