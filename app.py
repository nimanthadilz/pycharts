import tkinter as tk
from tkinter import ttk
from exceptions import ParseError
from ui.sidebar import Sidebar
from ui.output import Output
from parser import Parser
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
        menubar = tk.Menu(root)
        root['menu'] = menubar
        menuFile = tk.Menu(menubar)
        # File menu
        menubar.add_cascade(menu=menuFile, label="File")
        menuFile.add_command(label="New", command=self.menu_action, underline=0)
        menuFile.add_command(label="Exit", command=self.menu_action, underline=0)
        # Help menu
        menuHelp = tk.Menu(menubar)
        menubar.add_cascade(menu=menuHelp, label="Help")
        menuHelp.add_command(label="Tutorial", command=self.menu_action, underline=0)
        menuHelp.add_command(label="About", command=self.menu_action, underline=0)

        mainFrame = ttk.Frame(root, padding="3 3 12 12")
        mainFrame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.sidebar = Sidebar(mainFrame, self)
        self.output = Output(mainFrame)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(0, weight=1, minsize=500)
        mainFrame.columnconfigure(0, weight=3, minsize=800)
        mainFrame.columnconfigure(1, weight=1, minsize=300)

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
                self.message_handler.show_message(e.message, "Error")


if __name__=="__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
