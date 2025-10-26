from datetime import datetime


NORMALIZED_CANDLE_COLUMNS = {
        't': 'OpenTime_ms',
        'T': 'CloseTime_ms',
        'o': 'Open',
        'h': 'High',
        'l': 'Low',
        'c': 'Close',
        'v': 'Volume',
        'n': 'Trades',
        's': 'Symbol',
        'i': 'Interval',
}
RAW_CANDLE_COLS = list(NORMALIZED_CANDLE_COLUMNS.keys())

def timestamp_ms(datetime:datetime):
        return int(datetime.timestamp()*1000)