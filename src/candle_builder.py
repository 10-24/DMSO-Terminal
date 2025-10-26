from concurrent.futures import thread
from datetime import datetime
import pandas as pd
from helpers import RAW_CANDLE_COLS,timestamp_ms
import threading

# Ensure RAW_CANDLE_COLS is a pandas Index, Series, or appropriate type for the columns param
template_raw_candle = pd.DataFrame(columns=pd.Index(RAW_CANDLE_COLS))
class CandleBuilder:
    
    
    def __init__(self, interval_sec: int,on_candle_callback):
        self.on_candle_callback = on_candle_callback
        self.interval_sec = interval_sec
        self.buffer = {"OpenTime_ms": None, "trades":[]}
        self.prev_avg = None
        self._start_interval()
        
   
        
        
    def on_trade(self):
        trades = self.trade_buffer
        
        # Get the first trade's timestamp as the start of the current candle
        first_trade_time = trades[0]['time']
        candle_start_ms = (first_trade_time // interval_ms) * interval_ms
        
        # Group trades into the current candle
        candle_trades = []
        remaining_trades = []


    
    def _start_interval(self):
        open = timestamp_ms(datetime.now())
        self.buffer = {"OpenTime_ms": open, "trades":[]}
        
    
        
    def _emit_candle_(self):
        
        OpenTime_ms = self.buffer['OpenTime_ms']
        CloseTime_ms = timestamp_ms(datetime.now())
        
        trades:list = self.buffer['trades']
        
        if trades.__len__() == 0:
            return pd.DataFrame({"OpenTime_ms":OpenTime_ms,})
        
   
        
        
        
        
        volume = 0
        
        open_price = None
        close_price = None
        if trades.__len__() > 0:
            open_price = trades[0]['px']
            close_price = trades[-1]['px']
        
        volume = 0
        high = None
        low = None
        for trade in trades
        
        
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