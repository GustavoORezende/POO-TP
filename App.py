import customtkinter
from Models.models import User, Post
from Database.database import BancoDeDados, Feed

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

    
        self.title("Rede Social do Mark Zuckerberg")
        self.geometry("800x400")
        self.grid_columnconfigure(0, weight=1)
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=0, padx=15, pady=(15,0), sticky="ew")
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
       

    def button_callback(self):
        print("button pressed")

class myCommonButtons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.button = customtkinter.CTkButton(self, text="Login", command=self.login)
       
        
        

app = App()
app.mainloop()  