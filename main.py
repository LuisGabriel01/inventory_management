import tkinter as tk
from tkinter import ttk
from CRUD import *
class Notebook(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.frames = [] 
        self.pack(fill="both", expand=True)

    def add_tabs(self, frame, text):
        self.frames.append(frame)  
        self.add(frame, text=text)  
        
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

        self.create_tabs()

        self.notebook.bind("<<NotebookTabChanged>>",self.popular)
        
    def create_tabs(self):
        self.products = FramesMain(self.notebook, ("ID_Product", "Name", "Brand"),"products","#fcc668")
        self.moviments = FramesMain(self.notebook, ("ID_moviment","Date","Movement_type","Product_ID","Quantity","Employee"),'moviments',"#8bbcf0")
        self.stock = FramesMain(self.notebook, ("Product ID","Name","Brand","Quantity"),'stock',"#befac4")

        self.notebook.add_tabs(self.products, "Products")
        self.notebook.add_tabs(self.moviments, "Movements")
        self.notebook.add_tabs(self.stock, "Stock")

    def popular(self,event):
        id = self.notebook.select()
        frame = self.notebook.nametowidget(id)
        tree = frame.tree
        tree.delete(*tree.get_children())
        sql_select = dql(f"SELECT * FROM {frame.name}")
        for row in sql_select:
            tree.insert("","end",values=row)

class FramesMain(tk.Frame):
    def __init__(self, master, columns,name,bg):
        super().__init__(master)
        self.name = name
        self.columns = columns
        self.bg = bg
        self.frame = tk.Frame(self, borderwidth=3, width=1280, height=670, relief="groove", bg=bg)
        self.frame.place(relx=0, rely=1, anchor="sw")
        
        width_column = 600 // len(columns)

        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=31)
        for column in columns:
            self.tree.column(column, width=width_column, anchor="center", minwidth=50)
            self.tree.heading(column, text=column, anchor="center")
        self.tree.place(x=10, y=10)
        self.search_widgets()
    
    def search_widgets(self):

        self.search_frame = tk.LabelFrame(self,bg=self.bg,relief="groove")
        self.search_frame.place(x=940,y=80,anchor="center")

        text = self.name.capitalize()
        self.label_search = tk.Label(self.search_frame,text="Search",bg=self.bg,font=("Arial",15))
        self.label_search.grid(row=0,column=0,columnspan=3,pady=2,sticky="n")

        self.combobox_search = ttk.Combobox(self.search_frame,values=self.columns)
        self.combobox_search.grid(row=1,column=0,padx=5)

        self.entry_search = tk.Entry(self.search_frame,width=50)
        self.entry_search.grid(row=1,column=1)

        self.button_search = tk.Button(self.search_frame,text="Search",command=self.search_command)
        self.button_search.grid(row=1,column=2,padx=5,pady=5)
        
        self.entry_search.bind("<Return>",lambda event: (self.search_command()))

    def search_command(self):
        like = self.entry_search.get()
        column = self.combobox_search.get()
        if column:
            sql_consult = dql(f"SELECT * FROM {self.name} WHERE {column} LIKE '%{like}%'")
            self.tree.delete(*self.tree.get_children())
            for row in sql_consult:
                self.tree.insert("","end",values=row)

app = Root()
app.mainloop() 

# def popular(event):
#     global actual
#     tab_id = event.widget.select()
#     tab_info = event.widget.tab(tab_id)
#     sql_consult = dql(f"SELECT * FROM {tab_info['text']}")
#     frame = event.widget.nametowidget(tab_id)
#     tree = None
#     for i in frame.winfo_children():
#         if isinstance(i,ttk.Treeview):
#             tree = i
#             break
#     if tree:
#         tree.delete(*tree.get_children())
#     for row in sql_consult:
#         tree.insert("","end",values=row)
#     current_tab_id = notebook.select()
#     actual = notebook.nametowidget(current_tab_id)

# def search():
    

# # Creating the window
# root = tk.Tk()
# root.title("Inventory Managament")
# window_width = root.winfo_screenwidth()
# window_height = root.winfo_screenheight()
# root_largura = 1280
# root_altura = 720
# pos_y = (window_height - root_altura)//2
# pos_x = (window_width - root_largura)//2
# root.geometry(f"{root_largura}x{root_altura}+{pos_x}+{pos_y}")
# root.resizable(width=False,height=False)\

# #Notebook
# notebook = ttk.Notebook(root)
# notebook.pack()
# notebook.bind("<<NotebookTabChanged>>",popular)

# #Frame Products
# products = tk.Frame(notebook, borderwidth=3,width=1280, height=670, relief="groove",bg="#ADD8E6")
# products.place(relx=0, rely=1, anchor="sw")
# columns_products = ("ID_product","name","brande")
# tr_products = ttk.Treeview(products,columns=columns_products,show='headings',height=31)
# for i in columns_products:
#     tr_products.column(i,width=200,anchor="center",minwidth=50)
#     tr_products.heading(i,text=i,anchor="center")
# tr_products.place(x=10,y=10)
# # button_search = tk.Entry(products)
# # button_search.place(x=600,y=50)

# #Frame Movements
# moviments = tk.Frame(notebook, borderwidth=2,width=1280, height=670, relief="groove",bg="#90EE90")
# columns = get_columns("moviments")
# tr_moviments = ttk.Treeview(moviments,columns=columns,show='headings',height=31)
# for i in columns:
#     tr_moviments.column(i,width=100,anchor="center",minwidth=50)
#     tr_moviments.heading(i,text=i,anchor="center")
# tr_moviments.place(x=10,y=10)

# #Frame Stock
# stock = tk.Frame(notebook, borderwidth=4,width=1280, height=670, relief="groove",bg="#F5DEB3")
# columns_stock = get_columns("stock")
# tr_stock = ttk.Treeview(stock,columns=columns_stock,show='headings',height=31)
# for i in columns_stock:
#     tr_stock.column(i,width=150,anchor="center",minwidth=50)
#     tr_stock.heading(i,text=i,anchor="center")
# tr_stock.place(x=10,y=10)
# entry_search = tk.Entry(stock,width=40)
# entry_search.place(x=940,y=50,anchor="center")
# button_search = tk.Button(text="Nuossa")
# button_search.place(x=1060,y=77,anchor="w")


# frames_dict = {stock:"stock",moviments:"moviments",products:"products"} 
# for i,y in frames_dict.items():
#     notebook.add(i,text=f"{y}")




# root.mainloop()


