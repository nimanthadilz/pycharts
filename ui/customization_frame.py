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

        self.root = root
        self.app = app
        self.title = tk.StringVar(customization_frame, "")

        self.title_font_string = tk.StringVar(customization_frame, "Arial 20")
        self.title_font_family = "Arial"
        self.title_font_size = 20

        self.chart_font_string = tk.StringVar(customization_frame, "Arial 11")
        self.chart_font_family = "Arial"
        self.chart_font_size = 11

        self.colormap = tk.StringVar(customization_frame, "Blues")

        self.app.chart_properties = {
            "title": self.title.get(),
            "title_font_family": self.title_font_family,
            "title_font_size": self.title_font_size,
            "chart_font_family": self.chart_font_family,
            "chart_font_size": self.chart_font_size,
            "colormap": self.colormap.get()
        }

        frame_title_label = customtkinter.CTkLabel(master=customization_frame, text="Customization", text_font=("", 14), anchor="w")
        frame_title_label.grid(row=0, column=0, sticky=(tk.W), padx=(20,0))

        # Title
        title_label = customtkinter.CTkLabel(master=customization_frame, text="Title", text_font=("", 12)).grid(
            row=1, column=0, sticky=tk.W)
        title_entry = customtkinter.CTkEntry(master=customization_frame, placeholder_text="Enter title", text_font=("", 12), textvariable=self.title)
        title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Title font
        title_font_label = customtkinter.CTkLabel(master=customization_frame, text="Title font", text_font=("", 12)).grid(
            row=2, column=0, sticky=tk.W)
        title_font_entry = customtkinter.CTkEntry(master=customization_frame, text_font=("", 12), state="disabled", textvariable=self.title_font_string)
        title_font_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        title_font_select_btn = customtkinter.CTkButton(master=customization_frame, text="Change", text_font=("", 12), command=self.__show_title_font_selector)
        title_font_select_btn.grid(row=2, column=2)


        # Chart Font
        font_label = customtkinter.CTkLabel(master=customization_frame, text="Chart Font", text_font=("", 12)).grid(
            row=3, column=0, sticky=tk.W)
        font_entry = customtkinter.CTkEntry(master=customization_frame, text_font=("", 12), state="disabled", textvariable=self.chart_font_string)
        font_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))
        font_select_btn = customtkinter.CTkButton(master=customization_frame, text="Change", text_font=("", 12), command=self.__show_chart_font_selector)
        font_select_btn.grid(row=3, column=2)


        # Colormap
        colormap_label = customtkinter.CTkLabel(master=customization_frame, text="Color Map", text_font=("", 12)).grid(
            row=4, column=0, sticky=tk.W)
        colormaps = [
            'Greys',
            'Purples',
            'Blues',
            'Greens',
            'Oranges',
            'Reds',
            'YlOrBr',
            'YlOrRd',
            'OrRd',
            'PuRd',
            'RdPu',
            'BuPu',
            'GnBu',
            'PuBu',
            'YlGnBu',
            'PuBuGn',
            'BuGn',
            'YlGn'
        ]

        colormap_entry = customtkinter.CTkComboBox(master=customization_frame, values=colormaps, variable=self.colormap, text_font=("", 12))
        colormap_entry.configure(state="readonly", text_color="black")
        colormap_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

        # update button
        update_btn = customtkinter.CTkButton(master=customization_frame, text="Update", text_font=("", 12), command=self.update_chart)
        update_btn.grid(row=5, column=0)

        # reset button
        reset_btn = customtkinter.CTkButton(master=customization_frame, text="Reset", text_font=("", 12))
        reset_btn.grid(row=5, column=1, sticky=(tk.W))

    def update_chart(self):
        self.app.chart_properties = {
            "title": self.title.get(),
            "title_font_family": self.title_font_family,
            "title_font_size": self.title_font_size,
            "chart_font_family": self.chart_font_family,
            "chart_font_size": self.chart_font_size,
            "colormap": self.colormap.get()
        }
        self.app.update_chart()

    def __title_font_changed(self, font):
        font_properties = []
        if font[0] != "{":
            font_properties = font.split(" ")
        else:
            i = 1
            token = ""
            while font[i] != "}":
                token += font[i]
                i += 1
            font_properties.append(token)
            font_properties.extend(font[i + 1:].strip().split(" "))

        self.title_font_family = font_properties[0]
        self.title_font_size = int(font_properties[1])
        self.title_font_string.set(" ".join(font_properties))

    def __show_title_font_selector(self):
        self.root.tk.call("tk", "fontchooser", "configure", "-font", f"{{{self.title_font_family}}} {self.title_font_size}", "-command", self.root.register(self.__title_font_changed))
        self.root.tk.call("tk", "fontchooser", "show")
        
    def __chart_font_changed(self, font):
        font_properties = []
        if font[0] != "{":
            font_properties = font.split(" ")
        else:
            i = 1
            token = ""
            while font[i] != "}":
                token += font[i]
                i += 1
            font_properties.append(token)
            font_properties.extend(font[i + 1:].strip().split(" "))

        self.chart_font_family = font_properties[0]
        self.chart_font_size = int(font_properties[1])
        self.chart_font_string.set(" ".join(font_properties))

    def __show_chart_font_selector(self):
        self.root.tk.call("tk", "fontchooser", "configure", "-font", f"{{{self.chart_font_family}}} {self.chart_font_size}", "-command", self.root.register(self.__chart_font_changed))
        self.root.tk.call("tk", "fontchooser", "show")
        

