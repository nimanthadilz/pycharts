import tkinter as tk
from tkinter import ttk
from exceptions import ParseError
from ui.sidebar import Sidebar
from ui.output import Output
from input_parser import Parser
from chart_generator import ChartGenerator
from ui.message_handler import MessageHandler

class App:
    def __init__(self, root):
        self.parser = Parser()
        self.chart_generator = ChartGenerator()
        self.message_handler = MessageHandler(root)

        root.title("PyCharts++")
        root.state("zoomed")
        root.option_add("*tearOff", tk.FALSE)

        # Menubar
        menu_bar = tk.Menu(root)
        root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        # File menu
        menu_bar.add_cascade(menu=menu_file, label="File")
        menu_file.add_command(label="New", command=self.menu_action, underline=0)
        menu_file.add_command(label="Exit", command=self.menu_action, underline=0)
        # Help menu
        menu_help = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_help, label="Help")
        menu_help.add_command(label="Tutorial", command=self.menu_action, underline=0)
        menu_help.add_command(label="About", command=self.menu_action, underline=0)

        main_frame = ttk.Frame(root, padding="3 3 12 12")
        main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.sidebar = Sidebar(main_frame, self)
        self.output = Output(main_frame)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1, minsize=500)
        main_frame.columnconfigure(0, weight=3, minsize=800)
        main_frame.columnconfigure(1, weight=1, minsize=300)

    def menu_action(self):
        print("Menu itme clicked")

    def generate_chart(self, chart_type, file_obj):
        if file_obj == None:
            self.message_handler.show_message("No file selected.", "Error")
        elif file_obj.closed:
            self.message_handler.show_message("File is closed. Please reselect the file.", "Error")
        else:
            try:
                data = self.parser.parse(file_obj)
                self.parser.clear_nodes()
                figure = self.chart_generator.generate_chart(chart_type.get(), data)
                self.output.show_chart(figure)
                file_obj.close()
            except ParseError as e:
                self.parser.clear_nodes()
                self.message_handler.show_message(e.message, "Error")


if __name__=="__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
