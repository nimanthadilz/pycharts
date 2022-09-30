import customtkinter
import tkinter as tk
from tkinter import ttk

class CustomizationFrame:
    def __init__(self, root, app):
        customization_frame = customtkinter.CTkFrame(master=root)
        customization_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), ipadx=25, padx=25, pady=(25, 0))
        customization_frame.columnconfigure(0, weight=1)
        customization_frame.columnconfigure(1, weight=2)
        customization_frame.columnconfigure(2, weight=2, pad=20)
        customization_frame.rowconfigure(0, pad=20)
        customization_frame.rowconfigure(1, pad=20)
        customization_frame.rowconfigure(2, pad=20)
        customization_frame.rowconfigure(3, pad=20)
        customization_frame.rowconfigure(4, pad=20)
        customization_frame.rowconfigure(5, pad=20)

        self.app = app
        self.title = tk.StringVar(customization_frame, "")

        frame_title_label = customtkinter.CTkLabel(master=customization_frame, text="Customization", text_font=("", 14), anchor="w")
        frame_title_label.grid(row=0, column=0, sticky=(tk.W), padx=(20,0))

        # Title
        title_label = customtkinter.CTkLabel(master=customization_frame, text="Title", text_font=("", 12)).grid(
            row=1, column=0, sticky=tk.W)
        title_entry = customtkinter.CTkEntry(master=customization_frame, placeholder_text="Enter title", text_font=("", 12))
        title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Title font
        title_font_label = customtkinter.CTkLabel(master=customization_frame, text="Title font", text_font=("", 12)).grid(
            row=2, column=0, sticky=tk.W)
        title_font_entry = customtkinter.CTkEntry(master=customization_frame, text_font=("", 12), state="disabled")
        title_font_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        title_font_select_btn = customtkinter.CTkButton(master=customization_frame, text="Change", text_font=("", 12))
        title_font_select_btn.grid(row=2, column=2)


        # Font
        font_label = customtkinter.CTkLabel(master=customization_frame, text="Font", text_font=("", 12)).grid(
            row=3, column=0, sticky=tk.W)
        font_entry = customtkinter.CTkEntry(master=customization_frame, text_font=("", 12), state="disabled")
        font_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))
        font_select_btn = customtkinter.CTkButton(master=customization_frame, text="Change", text_font=("", 12))
        font_select_btn.grid(row=3, column=2)


        # Color
        color_label = customtkinter.CTkLabel(master=customization_frame, text="Color Range", text_font=("", 12)).grid(
            row=4, column=0, sticky=tk.W)
        color_entry = customtkinter.CTkEntry(master=customization_frame, text_font=("", 12), state="disabled")
        color_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
        color_select_btn = customtkinter.CTkButton(master=customization_frame, text="Change", text_font=("", 12))
        color_select_btn.grid(row=4, column=2)

        # update button
        update_btn = customtkinter.CTkButton(master=customization_frame, text="Update", text_font=("", 12))
        update_btn.grid(row=5, column=0)

        # reset button
        reset_btn = customtkinter.CTkButton(master=customization_frame, text="Reset", text_font=("", 12))
        reset_btn.grid(row=5, column=1, sticky=(tk.W))

