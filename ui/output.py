import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)


class Output:
    def __init__(self, root):
        styles = ttk.Style()
        styles.configure('Output.TFrame', borderwidth=5, relief="raised")

        outputFrame = ttk.Frame(root, padding="3 3 12 12", style="Output.TFrame")
        outputFrame["borderwidth"] = 2 
        outputFrame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        outputFrame.rowconfigure(0, weight=1)
        outputFrame.columnconfigure(0, weight=1)

        # Create the default figure
        fig = Figure(figsize=(8, 6), dpi=100, edgecolor="black", linewidth=1)

        # Embed the chart
        self.figure_canvas = FigureCanvasTkAgg(fig, master=outputFrame)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    def show_chart(self, figure):
        self.figure_canvas.figure = figure
        self.figure_canvas.draw()
        self.figure_canvas.flush_events()


