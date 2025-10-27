from dataclasses import dataclass

import pandas as pd

@dataclass
class Candle:
    open_timestamp: int
    close_timestamp: int
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    avg_price: float
    volume: int
    trades: int

    @staticmethod
    def from_raw(raw):
        pass
    
    def to_dataframe(self):
        return pd.DataFrame([self.__dict__])

@dataclass
class Trade:
    price: float
    timestamp_ms:int
    size:float;

    @staticmethod
    def from_raw(raw_trade):
        price = float(raw_trade['px'])
        timestamp_ms = raw_trade['time']
        size = float(raw_trade['sz'])  # 'sz' is size, not 'px' (price)
        return Trade(price,timestamp_ms,size)

        

