import datetime
import pandas as pd
from hyperliquid.info import Info
from hyperliquid.utils import constants
from pandas import DataFrame
from datetime import datetime
from src.helpers import timestamp_ms
from time_interval import TimeInterval
from helpers import NORMALIZED_CANDLE_MAP

class Dex:
    
    def __init__(self):
        self.info = Info(constants.TESTNET_API_URL)
        user_state = self.info.user_state("0xcd5051944f780a621ee62e39e493c489668acf4d")
        self.trade_buffers = {}  # Store trades for candle aggregation
    
    def subscribe(self,ticker:str,interval:TimeInterval,start:datetime,callback):
        
        candles = self.fetch_historical(ticker,interval,start)
        
        def on_new_candle(raw_candle):
            append_raw_candle(candles,raw_candle);
            callback(candles)
            
        self.info.subscribe({"type": "candle", "coin": "ETH", "interval": "1m"},on_new_candle)
        
 
            
        
        
    def fetch_historical(self,ticker:str,interval:TimeInterval,start:datetime):
        end = datetime.now()
        start_timestamp = timestamp_ms(start)
        end_timestamp = timestamp_ms(end)
        
        raw_candles_array = self.info.candles_snapshot(ticker,interval.value,start_timestamp,end_timestamp)
        
        return normalize_candles(raw_candles_array)
    
    def listen(self, ticker: str, interval_seconds: int, callback):
        
        interval_ms = interval_seconds * 1000
        
        # Initialize trade buffer for this ticker
        if ticker not in self.trade_buffers:
            self.trade_buffers[ticker] = []
        
        def on_trade(trades_data):
            """Called when new trades arrive"""
            for trade in trades_data:
                if trade['coin'] == ticker:
                    self.trade_buffers[ticker].append(trade)
                    candle = self._build_candle_from_trades(ticker, interval_ms)
                    if candle is not None:
                        callback(candle)
        
        # Subscribe to trades
        self.info.subscribe({"type": "trades", "coin": ticker}, on_trade)
    
    
   
    

def normalize_candles(raw_candles_array:list[dict]):
    raw_candles = pd.DataFrame(raw_candles_array)
    return raw_candles.rename(columns=NORMALIZED_CANDLE_MAP)

def append_raw_candle(candles:DataFrame,raw_candle:dict):
    new_candle = normalize_candles([raw_candle])
    pd.concat([candles,new_candle])
   


