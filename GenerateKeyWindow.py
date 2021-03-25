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
        
        self.info_label = tk.Label(master=self.window,text="Non prime numbers will be converted to nearest prime number",width=50)
        self.info_label.grid(row=1,column=0,columnspan=2,padx=2,pady=2)
        
        self.p_label = tk.Label(master=self.window,text="p: ")
        self.p_label.grid(row=2,column=0,padx=2,pady=2)
        
        self.p_entry = tk.Text(master=self.window,width=30,height=2)
        self.p_entry.grid(row=2,column=1,padx=2,pady=2)
        
        self.q_label = tk.Label(master=self.window,text="q: ")
        self.q_label.grid(row=3,column=0,padx=2,pady=2)
        
        self.q_entry = tk.Text(master=self.window,width=30,height=2)
        self.q_entry.grid(row=3,column=1,padx=2,pady=2)
        
        self.generate_button = tk.Button(master=self.window,text="Generate Key",width=20,command=self.GenerateKey)
        self.generate_button.grid(row=4,column=0,columnspan=2,padx=2,pady=2)
        
        self.randomize_button = tk.Button(master=self.window,text="Randomize Key",width=20,command=self.RandomizeKey)
        self.randomize_button.grid(row=5,column=0,columnspan=2,padx=2,pady=2)
        
    def GenerateKey(self):
        # Validation
        p = self.p_entry.get("1.0",tk.END)[:-1]
        q = self.q_entry.get("1.0",tk.END)[:-1]
        
        if (len(p)==0 or len(q)==0):
            self.AlertWindow("Please insert the numbers")
        else:
            p = int(p)
            q = int(q)

            p = ValidationPrime(p)
            q = ValidationPrime(q)

            # Generate key
            arr = GenerateKey(p, q)
            e = arr[0]
            d = arr[1]
            n = arr[2]

            # Save Key pair to file
            success = False
        
            public_filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select " + subject + " public key file",
                filetypes = [("Public key files (.pub)","*.pub")]
            )
            
            if (public_filename!=""):
                private_filename = fd.askopenfilename(
                    initialdir = public_filename[0:(public_filename.rfind('/')+1)],
                    title = "Select " + subject + " private key file",
                    filetypes = [("Private key files (.pri)","*.pri")]
                )
                
                if (private_filename!=""):
                    success = True 
            
            if (success):
                public_file = open(public_filename,"w")
                
                public_file.write(str(e))
                public_file.write(" ")
                public_file.write(str(n))
                
                public_file.close()
                
                private_file = open(private_filename,"w")
                
                private_file.write(str(d))
                private_file.write(" ")
                private_file.write(str(n))
                
                private_file.close()
        
        
    def RandomizeKey(self):
        # generate key
        out = RandomKey()
        p = out[0]
        q = out[1]
        e = out[2]
        d = out[3]
        n = out[4]

        self.p_entry.delete("1.0",tk.END)
        self.p_entry.insert("1.0",p)
        self.q_entry.delete("1.0",tk.END)
        self.q_entry.insert("1.0",q)

        # save ke file
        success = False
    
        public_filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select " + subject + " public key file",
            filetypes = [("Public key files (.pub)","*.pub")]
        )
        
        if (public_filename!=""):
            private_filename = fd.askopenfilename(
                initialdir = public_filename[0:(public_filename.rfind('/')+1)],
                title = "Select " + subject + " private key file",
                filetypes = [("Private key files (.pri)","*.pri")]
            )
            
            if (private_filename!=""):
                success = True 
        
        if (success):
            public_file = open(public_filename,"w")
            
            public_file.write(str(e))
            public_file.write(" ")
            public_file.write(str(n))
            
            public_file.close()
            
            private_file = open(private_filename,"w")
            
            private_file.write(str(d))
            private_file.write(" ")
            private_file.write(str(n))
            
            private_file.close()
    
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()