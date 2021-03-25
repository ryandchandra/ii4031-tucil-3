import tkinter as tk
import tkinter.scrolledtext as st

from GenerateKeyLib import *

class GenerateKeyWindow:
    def __init__(self,parent):
        self.parent = parent
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
        # Validation
        p = int(self.p_entry.get("1.0",tk.END)[:-1])
        q = int(self.q_entry.get("1.0",tk.END)[:-1])

        p = ValidationPrime(p)
        q = ValidationPrime(q)
        self.p_entry.delete("1.0",tk.END)
        self.p_entry.insert("1.0",p)
        self.q_entry.delete("1.0",tk.END)
        self.q_entry.insert("1.0",q)

        # generate key
        # save ke file
        #return "break"
        
    def RandomizeKey(self):
        # generate key
        # save ke file
        return "break"
    
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()
        
    def ConfirmationWindow(self,text):
        self.confirm_window = tk.Toplevel(self.parent)
        self.confirm_window.title("Confirm")
        
        tk.Label(master=self.confirm_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=self.confirm_window,text="OK",width=10,command=lambda text="OK":self.Confirm(text)).pack(pady=10)
        tk.Button(master=self.confirm_window,text="Cancel",width=10,command=lambda text="Cancel":self.Confirm(text)).pack(pady=10)
        
        self.confirm_window.grab_set()
        
    def Confirm(self,text):
        if (text=="OK"):
            # ganti nilai p q
            self.p_entry.insert("1.0",1)
            self.q_entry.insert("1.0",2)
            self.confirm_window.destroy()
        elif (text=="Cancel"):
            self.confirm_window.destroy()
            
        return "break"