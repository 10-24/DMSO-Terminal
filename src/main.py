import tkinter
from plot import plot
from dex import Dex
from time_interval import TimeInterval

def main():
    window = tkinter.Tk()
    window.title("DMSO Terminal")
    window.geometry("1000x1000")
    

    selected_view_width = TimeInterval.SECOND_30
    last_dataframe = None
    
    def on_candles(df):
        nonlocal last_dataframe
        # Store the latest dataframe
        last_dataframe = df
        # Use window.after() to ensure GUI updates happen in main thread
        # This prevents "main thread is not in main loop" error
        window.after(0, lambda: plot(window, df, ['avg_price'], selected_view_width))
    
    def rerender_plot():
        """Force rerender the plot with current view_width"""
        nonlocal last_dataframe
        nonlocal selected_view_width
        if last_dataframe is not None:
            df_copy = last_dataframe.copy()
            window.after(0, lambda df=df_copy: plot(window, df, ['avg_price'], selected_view_width))

    def render_buttons(frame:tkinter.Frame):
        # Clear all existing widgets in the frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        view_widths = [TimeInterval.SECOND_15, TimeInterval.SECOND_30, TimeInterval.MINUTE_1]

        for view_width in view_widths:
            def create_button_command(interval):
                def on_button_clicked():
                    nonlocal selected_view_width
                    selected_view_width = interval
                    rerender_plot()
                    render_buttons(frame)
                return on_button_clicked
            
            view_width_button = tkinter.Button(
                frame,
                text=view_width.value, 
                command=create_button_command(view_width),
                width=10,
                height=2,
                bg="#4CAF50",  # Green background
                fg="black" if view_width == selected_view_width else "white",  
                font=("Arial", 12, "bold")
            )
            view_width_button.pack(side=tkinter.LEFT, padx=5)
   
    # Create a frame for controls (top of window)
    control_frame = tkinter.Frame(window)
    control_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)
    
    
    render_buttons(control_frame)
    
    
    dex = Dex()
    dex.listen("ETH", 5, on_candles)
    
    window.mainloop()
    
    
   





if __name__ == "__main__":
    main()