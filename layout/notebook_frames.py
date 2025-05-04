from layout.products import *
from layout.movements import *
from layout.stock import *


class Notebook(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.frames = [] 
        self.pack(fill="both", expand=True)
        self.create_tabs()
        self.bind("<<NotebookTabChanged>>",self.popular_notebook)
        self.select(self.movements)

    def add_tabs(self, frame, text):
        self.frames.append(frame)  
        self.add(frame, text=text)
        
    def create_tabs(self):
        self.products = Products(self, ("ID_Product", "Name", "Brand"),"products","#fcc668")
        self.movements = Movements(self, ("ID_movement","Date","Movement_type","Product_ID","Quantity","Employee"),'movements',"#8bbcf0")
        self.stock = Stock(self, ("Product ID","Name","Brand","Quantity"),'stock',"#befac4")
        self.add_tabs(self.products, "Products")
        self.add_tabs(self.movements, "Movements")
        self.add_tabs(self.stock, "Stock")

    def popular_notebook(self,event=None):
        id = self.select()
        frame = self.nametowidget(id)
        frame.popular()
  


