from layout.framesmain import *

class Products(FramesMain):
    def __init__(self,master,columns,name,bg):
        super().__init__(master,columns,name,bg)
        self.center_frame.config(height=100,width=100)