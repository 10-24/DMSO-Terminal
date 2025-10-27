import rio

import pandas as pd
from typing import ClassVar
from datetime import datetime

from dex import Dex
from time_interval import TimeInterval
import plotly.graph_objects as go


class DMSOTerminal(rio.Component):
    """Main application component with Rio UI"""
    
    selected_view_width: TimeInterval = TimeInterval.SECOND_30
    dataframe: pd.DataFrame = pd.DataFrame()
    
    def __post_init__(self):
        """Called when the component is first created"""
        self.dex = Dex()
        
        def on_candles(df: pd.DataFrame):
            print(df)
            self.dataframe = df
        
        self.dex.listen("ETH", 5, on_candles)
    
    def get_filtered_dataframe(self) -> pd.DataFrame:
        """Filter dataframe based on selected view width"""
        if self.dataframe.empty:
            return self.dataframe
        
        # Filter by time window
        df = self.dataframe.copy()
        
        # Parse the window value (e.g., "15s", "1m")
        import re
        window_str = self.selected_view_width.value
        match = re.match(r'(\d+)([smhdwM])', window_str)
        
        if not match:
            return df
        
        amount = int(match.group(1))
        unit = match.group(2)
        
        # Convert to milliseconds
        multipliers = {
            's': 1000,
            'm': 60000,
            'h': 3600000,
            'd': 86400000,
            'w': 604800000,
            'M': 2592000000
        }
        
        window_ms = amount * multipliers.get(unit, 1000)
        latest_timestamp = df['open_timestamp'].max()
        cutoff_timestamp = latest_timestamp - window_ms
        
        return df[df['open_timestamp'] >= cutoff_timestamp]
    
    def on_view_width_selected(self, interval: TimeInterval):
        """Handle view width button click"""
        self.selected_view_width = interval
    
    def build(self) -> rio.Component:
        """Build the UI"""
        
        filtered_df = self.get_filtered_dataframe()
        
        # Create the plot
        if not filtered_df.empty and 'open_timestamp' in filtered_df.columns:
            # Convert timestamps to datetime
            timestamps = filtered_df['open_timestamp']
            dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]
            
            # Create Plotly figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=filtered_df['avg_price'],
                mode='lines',
                name='Average Price',
                line=dict(width=2)
            ))
            
            fig.update_layout(
                hovermode='x unified',
            )
            
            plot = rio.Plot(fig,min_height=30)
        else:
            plot = rio.Text("Waiting for data...",min_height=30)
        
        # Create view width buttons
        view_widths = [
            TimeInterval.SECOND_15,
            TimeInterval.SECOND_30,
            TimeInterval.MINUTE_1
        ]
        
        buttons = []
        for interval in view_widths:
            is_selected = interval == self.selected_view_width
            button = rio.Button(
                interval.value,
                on_press=lambda interval=interval: self.on_view_width_selected(interval),
                style="major" if is_selected else "minor",
                margin=1,
                
            )
            buttons.append(button)
        
        return rio.Column(
            plot,
            rio.Column(
                rio.Text("Width:"),
                rio.Row(
                    *buttons,
                    
                    spacing=0.1,
                    margin=0.1,
                )
            ),
            spacing=1,
            margin=1,
        )
        


def main():
    """Main entry point"""
    app = rio.App(build=DMSOTerminal)
    app.run_in_window()

if __name__ == "__main__":
    main()

