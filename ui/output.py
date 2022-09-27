import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)


class Output:
    def __init__(self, root):
        styles = ttk.Style()
        styles.configure('Output.TFrame', borderwidth=5, relief="raised")

        self.outputFrame = ttk.Frame(root, padding="3 3 12 12", style="Output.TFrame")
        self.outputFrame["borderwidth"] = 2 
        self.outputFrame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.outputFrame.rowconfigure(0, weight=1)
        self.outputFrame.columnconfigure(0, weight=1)

        # Create the default figure
        fig = Figure(figsize=(8, 6), dpi=100, edgecolor="black", linewidth=1)

        # Embed the chart
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.outputFrame)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    def show_chart(self, figure: Figure):
        figure.set_edgecolor("black")
        figure.set_linewidth(1)
        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.outputFrame)
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.figure_canvas.draw()


