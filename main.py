import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry
from tkinter import messagebox
import customtkinter as ctk
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

        self.notebook.bind("<<NotebookTabChanged>>",self.popular_notebook)

        self.notebook.select(self.moviments)
        
    def create_tabs(self):
        self.products = Products(self.notebook, ("ID_Product", "Name", "Brand"),"products","#fcc668")
        self.moviments = Moviments(self.notebook, ("ID_moviment","Date","Moviment_type","Product_ID","Quantity","Employee"),'moviments',"#8bbcf0")
        self.stock = Stock(self.notebook, ("Product ID","Name","Brand","Quantity"),'stock',"#befac4")

        self.notebook.add_tabs(self.products, "Products")
        self.notebook.add_tabs(self.moviments, "Moviments")
        self.notebook.add_tabs(self.stock, "Stock")

    def popular_notebook(self,event=None):
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
        self.frame = tk.Frame(self, borderwidth=3, width=1280, height=670, relief="groove")
        self.frame.place(relx=0, rely=1, anchor="sw")
        
        width_column = 600 // len(self.columns)

        self.tree = ttk.Treeview(self.frame, columns=self.columns, show='headings', height=31)
        for column in self.columns:
            self.tree.column(column, width=width_column, anchor="center", minwidth=50)
            self.tree.heading(column, text=column, anchor="center")
        self.tree.place(x=10, y=10)
        self.search_widgets()
        self.popular()
    
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

    def popular(self):
        self.tree.delete(*self.tree.get_children())
        sql_select = dql(f"SELECT * FROM {self.name}")
        for row in sql_select:
            self.tree.insert("","end",values=row)

class Products(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)

class Moviments(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)
        self.register_moviment()

    def register_moviment(self):
        def insert_moviment():
            date = self.register_dateentry.entry.get()
            product_id = self.id_product
            quantity = self.register_quantity_entry.get()
            employee = str(self.register_employee_entry.get())
            moviment_type = self.register_moviment_type_combobox.get()
            moviment_type = 1 if moviment_type == "Entry" else 0
            messagebox.askyesno("Confirmação","Are you sure about that?")
            dml(f"""
            INSERT INTO moviments (date,moviment_type,product_ID,quantity,employee)
            VALUES ('{date}',{moviment_type},{product_id},{quantity},'{employee}')
            """)

            self.popular()

        self.register_frame = tk.LabelFrame(self,bg=self.bg,relief="groove")
        self.register_frame.place(x=940,y=170,anchor="n",width=530,height=400)
        self.register_frame.pack_propagate(False)
        self.register_frame.grid_columnconfigure(0,weight=1)

        self.register_text = tk.Label(self.register_frame,text="Register Moviments",bg=self.bg,font=("Arial",16,"bold"))
        self.register_text.grid(row=0,column=0,pady=(0,20),sticky="n")

        self.search_product = tk.Button(self.register_frame,text="Select Product",command=self.top_products)
        self.search_product.grid(row=2,column=0,pady=(0,20))

        self.id_info = tk.Label(self.register_frame,text="id:")
        self.id_info.grid(row=3,column=0,sticky="w",padx=100)
        self.name_info = tk.Label(self.register_frame,text="name:")
        self.name_info.grid(row=4,column=0,sticky="w",padx=100)
        self.brand_info = tk.Label(self.register_frame,text="brand:")
        self.brand_info.grid(row=5,column=0,sticky="w",padx=100,pady=(0,20))

        self.register_dateentry = DateEntry(self.register_frame,bootstyle='secondary')
        self.register_dateentry.grid(row=7,column=0,sticky="w",padx=100,pady=(0,20))

        self.register_entrys_frames = tk.Frame(self.register_frame)
        self.register_entrys_frames.grid(row=9,column=0,sticky="w",padx=100,)

        self.register_quantity_text = tk.Label(self.register_entrys_frames,text="Quantity")
        self.register_quantity_text.grid(row=1,column=0,sticky="w")
        self.register_quantity_entry = tk.Entry(self.register_entrys_frames)
        self.register_quantity_entry.grid(row=1,column=1)

        self.register_employee_text = tk.Label(self.register_entrys_frames,text="Employee")
        self.register_employee_text.grid(row=2,column=0,sticky="w")
        self.register_employee_entry = tk.Entry(self.register_entrys_frames)
        self.register_employee_entry.grid(row=2,column=1)

        self.register_moviment_typetext = tk.Label(self.register_entrys_frames,text="Moviment Type")
        self.register_moviment_typetext.grid(row=3,column=0,sticky="w")
        self.register_moviment_type_combobox = ttk.Combobox(self.register_entrys_frames,values=["Entry","saída"])
        self.register_moviment_type_combobox.grid(row=3,column=1)

        self.register_button = tk.Button(self.register_frame,text="Register Moviment",command=insert_moviment)
        self.register_button.grid(row=10,column=0,pady=(20,0))

    def top_products(self):

        def popular_toptree():
            self.top_tree.delete(*self.top_tree.get_children())
            sqlconsult = dql("SELECT * FROM PRODUCTS")
            for row in sqlconsult:
                self.top_tree.insert("","end",values=row)

        def search_products():
            self.top_tree.delete(*self.top_tree.get_children())
            text = self.top_entry.get()
            column = self.top_combobox.get()
            sqlconsult = dql(f"SELECT * FROM PRODUCTS WHERE {column} LIKE '%{text}%'")
            for row in sqlconsult:
                self.top_tree.insert("","end",values=row)
        
        def select_item(event):
            try:
                selected_item = self.top_tree.focus()
                self.info_selected = self.top_tree.item(selected_item)['values']
                self.text_selected = f"Produto selecionado: \nID: {self.info_selected[0]},\nName: {self.info_selected[1]},\nBrand: {self.info_selected[2]}"
                self.top_info_select.config(text=self.text_selected)
            except:
                pass
        
        def select_confirm():
            self.id_product = self.info_selected[0]
            self.id_info.config(text=f"Id: {self.id_product}")
            self.name_info.config(text=f"Name: {self.info_selected[1]}")
            self.brand_info.config(text=f"Brand: {self.info_selected[2]}")
            self.top.destroy()
        
        self.top = tk.Toplevel()
        self.top.geometry("600x600+1050+300")
        self.top.grab_set()
        self.top.resizable(height=False,width=False)

        self.top_frame = tk.Frame(self.top,width=600,height=150,bg="#ad9e72")
        self.top_frame.place(x=300,y=75,anchor="center")
        columns = ("ID_Product","Name","Brand")

        self.top_text = tk.Label(self.top_frame,text="Search for a product")
        self.top_text.grid(row=0,column=0,columnspan=3,pady=2,sticky="n")

        self.top_entry = tk.Entry(self.top_frame,width=30)
        self.top_entry.grid(row=2,column=1)
        self.top_entry.bind("<Return>",lambda event: search_products())

        self.top_button_search = tk.Button(self.top_frame,text="Search",command=search_products)
        self.top_button_search.grid(row=2,column=2,padx=5)
        
        self.top_button_confirm = tk.Button(self.top_frame,text="Confirm",command=select_confirm)
        self.top_button_confirm.grid(row=3,column=1,columnspan=3)

        self.top_combobox = ttk.Combobox(self.top_frame,values=("ID_Product","Name","Brand"))
        self.top_combobox.set("Name")
        self.top_combobox.grid(row=2,column=0,padx=5)

        self.top_info_select = tk.Label(self.top_frame,text="Produto Selecionado: Nenhum",justify="left")
        self.top_info_select.grid(row=3,column=0,columnspan=3,pady=5,padx=(0,100))

        self.top_tree_frame = tk.Frame(self.top)
        self.top_tree_frame.place(x=300,y=150,anchor="n")
        self.top_tree = ttk.Treeview(self.top_tree_frame, columns=columns, show='headings', height=31)
        for i in columns:
            self.top_tree.column(i,anchor="center",width=200)
            self.top_tree.heading(i,text=i,anchor="center")
        self.top_tree.grid(row=0,column=0)
        self.top_tree.bind('<<TreeviewSelect>>',select_item)

        popular_toptree()

class Stock(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)
        

app = Root()
app.mainloop() 
