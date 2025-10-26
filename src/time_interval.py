from enum import Enum

class TimeInterval(Enum):
    """
    Supported time intervals (klines/candles) for the Hyperliquid API.
    These values are used in the `interval` parameter for fetching historical data.
    """
    
    # Seconds
    SECOND_1 = "1s"
    SECOND_15 = "15s"
    SECOND_30 = "30s"
    
    # Minutes
    MINUTE_1 = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    
    # Hours
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    
    # Days/Weeks/Months
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M" # Note: Capital 'M' for Month