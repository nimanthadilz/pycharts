import tkinter as tk
from tkinter import W, ttk
from ui.data_input_frame import DataInputFrame


class Sidebar:
    def __init__(self, root, app):
        styles = ttk.Style()
        styles.configure('Danger.TFrame', borderwidth=5, relief="raised")

        sidebar_frame = ttk.Frame(root, padding="3 3 12 12", style="Danger.TFrame")
        sidebar_frame["borderwidth"] = 2 
        sidebar_frame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        sidebar_frame.rowconfigure(1, weight=1)
        sidebar_frame.columnconfigure(0, weight=1)

        nameLabel = ttk.Label(sidebar_frame, text="Sidebar")
        nameLabel.grid(row=0, column=0, sticky=W)

        DataInputFrame(sidebar_frame, app)


