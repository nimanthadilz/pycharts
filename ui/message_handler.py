from tkinter import messagebox

class MessageHandler:
    def __init__(self, root):
        self.root = root

    def show_message(self, message, type):
        if type=="Error":
            messagebox.showerror("Error", message)
        elif type=="Info":
            messagebox.showinfo("Info", message)
            
        

