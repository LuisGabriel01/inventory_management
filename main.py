import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap.widgets import DateEntry
from database.CRUD import *
from layout.notebook_frames import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()
        root_largura = 1280
        root_altura = 720
        pos_y = (window_height - root_altura)//2
        pos_x = (window_width - root_largura)//2
        self.geometry(f"{root_largura}x{root_altura}+{pos_x}+{pos_y}")
        self.resizable(width=False, height=False)
        self.notebook = Notebook(self)


if __name__ == "__main__":
    app = Root()
    app.mainloop() 
