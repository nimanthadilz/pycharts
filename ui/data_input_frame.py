import tkinter as tk
from tkinter import E, W, ttk
from tkinter import filedialog as fd
import os
from exceptions import ParseError

class DataInputFrame:
    def __init__(self, root, app):
        input_frame = ttk.LabelFrame(root, text="Data")
        input_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        input_frame.columnconfigure(0)
        input_frame.columnconfigure(1)

        self.app = app
        self.file_name = tk.StringVar(input_frame, "No file.")
        self.chart_type = tk.StringVar(input_frame, "Treemap")
        self.file_obj = None


        file_label = ttk.Label(input_frame, text="File Name").grid(
            row=0, column=0, sticky=W, padx=(0, 20))
        file_name_label = ttk.Label(input_frame, textvariable=self.file_name)
        file_name_label.grid(row=0, column=1, sticky=W, padx=(0, 20))

        browse_btn = ttk.Button(input_frame, text="Select", command=self._file_select)
        browse_btn.grid(row=0, column=2, sticky=W)

        chart_type_label = ttk.Label(input_frame, text="Chart Type")
        chart_type_label.grid(row=1, column=0, sticky=W, padx=(0, 20), pady=(10, 0))
        chart_type_menu = ttk.Combobox(input_frame, values=["Treemap", "Icicle", "Sunburst"], textvariable=self.chart_type)
        chart_type_menu.grid(row=1, column=1, sticky=W, pady=(10, 0))
        chart_type_menu.state(["readonly"])

        generate_btn = ttk.Button(input_frame, text="Generate", command=self._generate_btn_click_handler)
        generate_btn.grid(row=2, column=1, sticky=W, pady=(10, 0))

    def _file_select(self):
        file_types = (("CSV files", "*.csv"), ("All files", "*.*"))

        file_obj = fd.askopenfile(filetypes=file_types)
        self._set_file_name(os.path.basename(file_obj.name))
        self.file_obj = file_obj

    def _set_file_name(self, name):
        self.file_name.set(name)
        
    def _generate_btn_click_handler(self):
        self.app.generate_chart(self.chart_type, self.file_obj)

