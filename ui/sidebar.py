import customtkinter
import tkinter as tk
from tkinter import W, ttk
from ui.customization_frame import CustomizationFrame
from ui.data_input_frame import DataInputFrame


class Sidebar:
    def __init__(self, root, app):
        # styles = ttk.Style()
        # styles.configure('Danger.TFrame', borderwidth=5, relief="raised")

        sidebar_frame = customtkinter.CTkFrame(master=root)
        sidebar_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), ipadx=25)
        sidebar_frame.rowconfigure(1)
        sidebar_frame.rowconfigure(2)
        sidebar_frame.columnconfigure(0, weight=1)

        nameLabel = customtkinter.CTkLabel(master=sidebar_frame, text="Sidebar", text_font=("", 16))
        nameLabel.grid(row=0, column=0, sticky=W, pady=(15, 0))
        DataInputFrame(sidebar_frame, app)
        CustomizationFrame(sidebar_frame, app)

