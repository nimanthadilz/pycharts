import customtkinter
import tkinter as tk
from tkinter import E, W, ttk
from tkinter import filedialog as fd
import os

class DataInputFrame:
    def __init__(self, root, app):
        input_frame = customtkinter.CTkFrame(master=root)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), ipadx=25, padx=25, pady=(25, 0))
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)
        input_frame.rowconfigure(0, pad=20)
        input_frame.rowconfigure(1, pad=20)
        input_frame.rowconfigure(2, pad=20)

        self.app = app
        self.file_name = tk.StringVar(input_frame, "No file.")
        self.chart_type = tk.StringVar(input_frame, "Treemap")
        self.file_obj = None

        frame_title_label = customtkinter.CTkLabel(master=input_frame, text="Data", text_font=("", 14), anchor="w")
        frame_title_label.grid(row=0, column=0, sticky=(tk.W), padx=(20,0))

        file_label = customtkinter.CTkLabel(master=input_frame, text="File Name", text_font=("", 12)).grid(
            row=1, column=0, sticky=W)
        file_name_label = customtkinter.CTkLabel(master=input_frame, textvariable=self.file_name, text_font=("", 12))
        file_name_label.grid(row=1, column=1, sticky=W)

        browse_btn = customtkinter.CTkButton(master=input_frame, text="Select", command=self._file_select, text_font=("", 12))
        browse_btn.grid(row=1, column=2, sticky=W)

        chart_type_label = customtkinter.CTkLabel(master=input_frame, text="Chart Type", text_font=("", 12))
        chart_type_label.grid(row=2, column=0, sticky=W)
        chart_type_menu = customtkinter.CTkComboBox(master=input_frame, values=["Treemap", "Icicle", "Sunburst"], variable=self.chart_type, text_font=("", 12))
        chart_type_menu.configure(state="readonly", text_color="black")
        chart_type_menu.grid(row=2, column=1, sticky=W)

        generate_btn = customtkinter.CTkButton(master=input_frame, text="Generate", command=self._generate_btn_click_handler, text_font=("", 12))
        generate_btn.grid(row=2, column=2, sticky=W)

    def _file_select(self):
        file_types = (("CSV files", "*.csv"), ("All files", "*.*"))

        file_obj = fd.askopenfile(filetypes=file_types)
        if file_obj != None:
            self._set_file_name(os.path.basename(file_obj.name))
            self.file_obj = file_obj

    def _set_file_name(self, name):
        self.file_name.set(name)
        
    def _generate_btn_click_handler(self):
        self.app.generate_chart(self.chart_type, self.file_obj)

