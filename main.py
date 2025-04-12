import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from CRUD import *
import time
dados_temporarios = {}

def show_tables(variable):
    global tr,scroll,comboget,row
    try:
        tr.destroy()
    except:
        pass

    try:
        scroll.destroy()
    except:
        pass
    
    comboget = combobox.get()
    columns = get_columns(comboget)
    tr = ttk.Treeview(root,columns=columns,show='headings',height=31)
    for i in columns:
        tr.column(i,width=100,anchor="center",minwidth=50)
        tr.heading(i,text=i,anchor="center")
    tr.place(x=10,y=40)

    row = len(columns)
    for row in dql(f"SELECT * FROM {comboget}"):
        tr.insert("","end",values=row)

    scroll = ttk.Scrollbar(root,orient=tk.VERTICAL,command=tr.yview)
    scroll.place(x=0,y=40,height=650)

    tr.configure(yscrollcommand=scroll.set)

def get_selecteditem():
    currentitem = tr.focus()
    print(tr.item(currentitem)["values"])
    
#Creating the window
root = tk.Tk()
root.title("Inventory Managament")
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root_largura = 1280
root_altura = 720
pos_y = (window_height - root_altura)//2
pos_x = (window_width - root_largura)//2
root.geometry(f"{root_largura}x{root_altura}+{pos_x}+{pos_y}")
root.resizable(width=False,height=False)

#Tree Frame
tree_frame = tk.Frame()
tree_frame.pack(ipady=50)

# Tree View
tr = ttk.Treeview(root,columns=("id","name","brand"),show='headings',height=31)
tr.column('id',width=50,anchor="center")
tr.column('name',minwidth=50)
tr.column('brand',minwidth=50)
tr.heading('id',text="",anchor="center")
tr.heading('name',text="")
tr.heading('brand',text="")
tr.place(relx=0.19,rely=0.5,anchor="center")

#COMBOBOX TABLES
combobox = ttk.Combobox(root)
combobox['values'] = ("products","movements","stock")
combobox.place(relx=0.15,rely=0.015)
combobox.bind("<<ComboboxSelected>>",show_tables)


root.mainloop()

