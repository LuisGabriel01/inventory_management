from layout.framesmain import *

class Products(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)
        self.center_frame.place_configure(height=150)
        self.center_text.config(text="Register Product")
        self.register_product = self.center_text
        self.combobox_search.set("Name")
        self.register_products()


    def register_products(self):
        def insert_product():
            name = self.register_name_entry.get()
            brand = self.register_brand_entry.get()
            if name == "" or brand == "":
                messagebox.showerror("Erro","Por favor preencha todos os campos")
                return
            dml(f"""
            INSERT INTO products (name,brand)
            VALUES ('{name}','{brand}')
            """)
            self.popular()
        
        self.register_name_text = tk.Label(self.center_frame,text="Name:")
        self.register_name_text.grid(row=3,column=0,sticky="w",padx=100,pady=(20,0))
        self.register_name_entry = tk.Entry(self.center_frame)
        self.register_name_entry.grid(row=3,column=0,sticky="e",padx=100,pady=(20,0))

        self.register_brand_text = tk.Label(self.center_frame,text="Brand:")
        self.register_brand_text.grid(row=4,column=0,sticky="w",padx=100)
        self.register_brand_entry = tk.Entry(self.center_frame)
        self.register_brand_entry.grid(row=4,column=0,sticky="e",padx=100)

        self.center_button.config(text="Register Product",command=insert_product)
        self.center_button.grid(row=5,column=0,pady=(20,0))
