from tkinter import Tk
import tkinter
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import dates as mdates
from datetime import datetime
from typing import Optional

from time_interval import TimeInterval

# Global variables to store plot components
_canvas_widget: Optional[tkinter.Widget] = None
_figure: Optional[Figure] = None
_ax: Optional[Axes] = None
_canvas: Optional[FigureCanvasTkAgg] = None

def plot(container:Tk, df:DataFrame, cols:list[str],width:TimeInterval):
    """Plot a DataFrame as a line chart using matplotlib"""
    global _canvas_widget, _figure, _ax, _canvas
    
    # Don't plot if dataframe is empty
    if df.empty or len(df) == 0:
        return
    
    # Filter dataframe to show only the last N seconds/minutes
    df = filter_by_time_window(df, width)
    
    # Don't plot if dataframe is empty after filtering
    if df.empty or len(df) == 0:
        return
    
    # Create figure if it doesn't exist
    if _figure is None or _ax is None:
        _figure, _ax = plt.subplots(figsize=(10, 6))
        
        # Configure date formatting for x-axis
        _ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        _ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        _ax.set_xlabel('Time')
        _ax.set_ylabel('Price')
        _ax.grid(True)
        
        # Embed in tkinter
        _canvas = FigureCanvasTkAgg(_figure, container)
        _canvas_widget = _canvas.get_tk_widget()
        _canvas_widget.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    # Clear existing lines before plotting new data
    if _ax is not None:
        _ax.clear()
        
        # Configure date formatting for x-axis
        _ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        _ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        _ax.set_xlabel('Time')
        _ax.set_ylabel('Price')
        _ax.grid(True)
        
        # Convert Unix timestamps (in milliseconds) to datetime objects
        timestamps = df['open_timestamp']
        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]
        
        # Plot each column
        for col in cols:
            if col in df.columns:
                _ax.plot(dates, df[col], label=col, linewidth=2)
        
        _ax.legend()
        
        # Rotate date labels for better readability
        plt.setp(_ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Adjust layout to prevent label clipping
        _figure.tight_layout()
        
        # Redraw the canvas
        if _canvas is not None:
            _canvas.draw()

def filter_by_time_window(df: DataFrame, window: TimeInterval) -> DataFrame:
    """Filter dataframe to show only the last N seconds/minutes based on window"""
    import re
    
    if df.empty or 'open_timestamp' not in df.columns:
        return df
    
    # Parse the window value (e.g., "15s", "1m")
    window_str = window.value
    match = re.match(r'(\d+)([smhdwM])', window_str)
    
    if not match:
        # Default to showing all data
        return df
    
    amount = int(match.group(1))
    unit = match.group(2)
    
    # Convert to milliseconds
    multipliers = {
        's': 1000,           # seconds to milliseconds
        'm': 60000,          # minutes to milliseconds
        'h': 3600000,        # hours to milliseconds
        'd': 86400000,       # days to milliseconds
        'w': 604800000,      # weeks to milliseconds
        'M': 2592000000      # months to milliseconds (approx 30 days)
    }
    
    window_ms = amount * multipliers.get(unit, 1000)
    
    # Get the latest timestamp
    latest_timestamp = df['open_timestamp'].max()
    
    # Filter to show only data within the window
    cutoff_timestamp = latest_timestamp - window_ms
    filtered_df = df[df['open_timestamp'] >= cutoff_timestamp]
    
    return filtered_df
  
    