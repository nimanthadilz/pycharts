import tkinter as tk
from tkinter import W, ttk
from ui.data_input_frame import DataInputFrame


class Sidebar:
    def __init__(self, root, app):
        styles = ttk.Style()
        styles.configure('Danger.TFrame', borderwidth=5, relief="raised")

        sidebarFrame = ttk.Frame(root, padding="3 3 12 12", style="Danger.TFrame")
        sidebarFrame["borderwidth"] = 2 
        sidebarFrame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        sidebarFrame.rowconfigure(1, weight=1)
        sidebarFrame.columnconfigure(0, weight=1)

        nameLabel = ttk.Label(sidebarFrame, text="Sidebar")
        nameLabel.grid(row=0, column=0, sticky=W)

        DataInputFrame(sidebarFrame, app)


