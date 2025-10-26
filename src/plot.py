from tkinter import Tk
import tkinter
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def plot(container:Tk, df:DataFrame):
    """Plot a DataFrame as a line chart using matplotlib"""
    # Create a figure
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df['X'], df['Y'], 'b-', linewidth=2)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Sample Plot')
    ax.grid(True)
    
    # Embed in tkinter
    canvas = FigureCanvasTkAgg(fig, container)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    return canvas
    