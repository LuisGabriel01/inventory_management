from layout.framesmain import *
from ttkbootstrap.widgets import DateEntry
from tkinter import messagebox

class Moviments(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)
        self.register_moviment()
        self.center_button.config(text="Select Product",command=self.top_products)
        self.search_button = self.center_button
        del self.center_button
        self.center_text.config(text="Register Moviment")

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

        self.id_info = tk.Label(self.center_frame,text="id:")
        self.id_info.grid(row=3,column=0,sticky="w",padx=100,pady=(20,0))
        self.name_info = tk.Label(self.center_frame,text="name:")
        self.name_info.grid(row=4,column=0,sticky="w",padx=100)
        self.brand_info = tk.Label(self.center_frame,text="brand:")
        self.brand_info.grid(row=5,column=0,sticky="w",padx=100,pady=(0,20))



        self.register_entrys_frames = tk.Frame(self.center_frame)
        self.register_entrys_frames.grid(row=6,column=0,sticky="w",padx=100,pady=(0,20))

        self.register_dateentry = DateEntry(self.center_frame,bootstyle='secondary')
        self.register_dateentry.grid(row=7,column=0,padx=0,pady=(0,20))

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

        self.register_button = tk.Button(self.center_frame,text="Register Moviment",command=insert_moviment,height=2,anchor="center")
        self.register_button.grid(row=8,column=0,pady=(20,0))

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