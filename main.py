import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from CRUD import *

def trade_frames(frame):
    global actual
    actual.place_forget()
    if frame == "stock":
        stock.place(relx=0, rely=1, anchor="sw")
        actual = stock
        popular(stock,"stock")
    elif frame == "products":
        products.place(relx=0, rely=1, anchor="sw")
        actual = products
        popular(products,"products")
    elif frame == "moviments":
        moviments.place(relx=0, rely=1, anchor="sw")
        actual = moviments
        popular(moviments,"moviments")

def popular(frame,str):
    for widget in frame.winfo_children():
        if isinstance(widget,ttk.Treeview):
            tree = widget
            break
    for item in tree.get_children():
        tree.delete(item)
    for row in dql(f"SELECT * FROM {str}"):
        tree.insert("","end",values=row)

# Creating the window
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

#Buttons main and Frame
buttonsframe = tk.Frame(root,borderwidth=3,width=1280,height=50,relief="solid")
buttonsframe.place(relx=0.5,rely=0,anchor="n")
products_active = tk.Button(buttonsframe,text="Products",command=lambda:trade_frames("products"))
products_active.place(relx=0.4,rely=0.5,anchor="center")
moviments_active = tk.Button(buttonsframe,text="Moviments",command=lambda:trade_frames("moviments"))
moviments_active.place(relx=0.456,rely=0.5,anchor="center")
stock_active = tk.Button(buttonsframe,text="Estoque",command=lambda:trade_frames("stock"))
stock_active.place(relx=0.512,rely=0.5,anchor="center")


#Frame Products
products = tk.Frame(root, borderwidth=3,width=1280, height=670, relief="groove",bg="#ADD8E6")
products.place(relx=0, rely=1, anchor="sw")
actual = products
columns_products = ("ID_product","name","brande")
tr_products = ttk.Treeview(products,columns=columns_products,show='headings',height=31)
for i in columns_products:
    tr_products.column(i,width=100,anchor="center",minwidth=50)
    tr_products.heading(i,text=i,anchor="center")
tr_products.place(x=10,y=10)

#Frame Movements
moviments = tk.Frame(root, borderwidth=2,width=1280, height=670, relief="groove",bg="#90EE90")
columns = get_columns("moviments")
tr_moviments = ttk.Treeview(moviments,columns=columns,show='headings',height=31)
for i in columns:
    tr_moviments.column(i,width=100,anchor="center",minwidth=50)
    tr_moviments.heading(i,text=i,anchor="center")
tr_moviments.place(x=10,y=10)

#Frame Stock
stock = tk.Frame(root, borderwidth=4,width=1280, height=670, relief="groove",bg="#F5DEB3")
columns_stock = get_columns("stock")
tr_stock = ttk.Treeview(stock,columns=columns_stock,show='headings',height=31)
for i in columns_stock:
    tr_stock.column(i,width=100,anchor="center",minwidth=50)
    tr_stock.heading(i,text=i,anchor="center")
    print(i)
tr_stock.place(x=10,y=10)

print(products.winfo_children())
root.mainloop()

