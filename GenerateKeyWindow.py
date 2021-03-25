import tkinter as tk
import tkinter.scrolledtext as st

class GenerateKeyWindow:
    def __init__(self,parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Key")
        
        self.title_label = tk.Label(master=self.window,text="Please insert two prime numbers",width=50)
        self.title_label.grid(row=0,column=0,columnspan=2,padx=2,pady=2)
        
        self.p_label = tk.Label(master=self.window,text="p: ")
        self.p_label.grid(row=1,column=0,padx=2,pady=2)
        
        self.p_entry = tk.Text(master=self.window,width=30,height=2)
        self.p_entry.grid(row=1,column=1,padx=2,pady=2)
        
        self.q_label = tk.Label(master=self.window,text="q: ")
        self.q_label.grid(row=2,column=0,padx=2,pady=2)
        
        self.q_entry = tk.Text(master=self.window,width=30,height=2)
        self.q_entry.grid(row=2,column=1,padx=2,pady=2)
        
        self.generate_button = tk.Button(master=self.window,text="Generate Key",width=20,command=self.GenerateKey)
        self.generate_button.grid(row=3,column=0,columnspan=2,padx=2,pady=2)
        
        self.randomize_button = tk.Button(master=self.window,text="Randomize Key",width=20,command=self.RandomizeKey)
        self.randomize_button.grid(row=4,column=0,columnspan=2,padx=2,pady=2)
        
    def GenerateKey(self):
        # validasi
        # generate key
        # save ke file
        return "break"
        
    def RandomizeKey(self):
        # generate key
        # save ke file
        return "break"