import tkinter as tk
from tkinter import ttk
from database.CRUD import *

class FramesMain(tk.Frame):
    def __init__(self, master, columns,name,bg):
        super().__init__(master)
        self.name = name
        self.columns = columns
        self.bg = bg
        self.frame = tk.Frame(self, borderwidth=3, width=1280, height=670, relief="groove")
        self.frame.place(relx=0, rely=1, anchor="sw")
        
        width_column = 600 // len(self.columns)

        self.tree = ttk.Treeview(self.frame, columns=self.columns, show='headings', height=40)
        for column in self.columns:
            self.tree.column(column, width=width_column, anchor="center", minwidth=50)
            self.tree.heading(column, text=column, anchor="center")
        self.tree.place(x=10, y=10)
        self.search_widgets()
        self.popular()

        
        self.center_frame = tk.LabelFrame(self,bg=self.bg,relief="groove")
        self.center_frame.place(x=940,y=350,anchor="center",width=530,height=400)
        self.center_frame.grid_columnconfigure(0,weight=1)

        self.center_text = tk.Label(self.center_frame,text="Text",bg=self.bg,font=("Arial",16,"bold"))
        self.center_text.grid(row=1,column=0)

        self.center_button = tk.Button(self.center_frame,text="Text")
        self.center_button.grid(row=2,column=0,pady=(35,0))

    def search_widgets(self):
        def search_command():
            like = self.entry_search.get()
            column = self.combobox_search.get()
            if column:
                sql_consult = dql(f"SELECT * FROM {self.name} WHERE {column} LIKE '%{like}%'")
                self.tree.delete(*self.tree.get_children())
                for row in sql_consult:
                    self.tree.insert("","end",values=row)        
        self.search_frame = tk.LabelFrame(self,bg=self.bg,relief="groove")
        self.search_frame.place(x=940,y=80,anchor="center")

        text = self.name.capitalize()
        self.search_text = tk.Label(self.search_frame,text="Search",bg=self.bg,font=("Arial",15))
        self.search_text.grid(row=0,column=0,columnspan=3,pady=2,sticky="n")

        self.combobox_search = ttk.Combobox(self.search_frame,values=self.columns)
        self.combobox_search.grid(row=1,column=0,padx=5)

        self.entry_search = tk.Entry(self.search_frame,width=50)
        self.entry_search.grid(row=1,column=1)

        self.button_search = tk.Button(self.search_frame,text="Search",command=search_command)
        self.button_search.grid(row=1,column=2,padx=5,pady=5)
        
        self.entry_search.bind("<Return>",lambda event: (search_command()))

    def popular(self,event=None):
        self.tree.delete(*self.tree.get_children())
        sql_select = dql(f"SELECT * FROM {self.name}")
        for row in sql_select:
            self.tree.insert("","end",values=row)