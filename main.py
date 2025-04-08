import tkinter as tk

dados_temporarios = {}

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

#Texto principal
text_main = tk.Label(root,text="Bem vindo ao meu primeiro programa",font=("Arial",25))
text_main.place(relx=0.5,rely=0.05,anchor="center")
root.mainloop()


