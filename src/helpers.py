from datetime import datetime


NORMALIZED_CANDLE_MAP = {
        't': 'open_timestamp',
        'T': 'close_timestamp',
        'o': 'open_price',
        'h': 'high',
        'l': 'low',
        'c': 'close_price',
        'v': 'volume',
        'n': 'trades',
}


CANDLE_COLS = list(NORMALIZED_CANDLE_MAP.keys()).append('avg_price')

def timestamp_ms(datetime:datetime):
        return int(datetime.timestamp()*1000)