import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import math

class FileHandlingWindow:
    def __init__(self,parent):
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title("Encrypt/Decrypt File")
        
        self.file = ""
        self.key = ""
        self.e_key = ""
        self.d_key = ""
        self.n_key = ""

        # Define elements
        self.file_label = tk.Label(master=self.window,text="File : " + self.file,width=50)
        self.file_label.grid(row=0,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.key_label = tk.Label(master=self.window,text="Key : " + self.key,width=50)
        self.key_label.grid(row=1,column=0,columnspan=2,sticky="we",padx=120,pady=2)

        self.e_key_label = tk.Label(master=self.window,text="e: " + self.e_key,width=50)
        self.e_key_label.grid(row=3,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.d_key_label = tk.Label(master=self.window,text="d: -")
        self.d_key_label.grid(row=4,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.n_key_label = tk.Label(master=self.window,text="n: -")
        self.n_key_label.grid(row=5,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        
        # Button list
        tk.Button(master=self.window,text="Choose File",width=20,command=self.ChooseFile).grid(row=6,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Choose Key",width=20,command=self.ChooseKey).grid(row=7,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Encrypt and Save",width=20,command=self.SaveEncryptedFile).grid(row=8,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Decrypt and Save",width=20,command=self.SaveDecryptedFile).grid(row=9,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Unselect File",width=20,command=self.UnselectFile).grid(row=10,column=0,columnspan=2,pady=2)
        
    def ChooseFile(self):
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select  file",
            filetypes = [("All files","*.*")],
        )
        
        if (filename!=""):
            self.file_label["text"] = "File : " + filename
            self.file = filename

    def ChooseKey(self):
        success = False
    
        public_filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select public key file",
            filetypes = [("Public key files (.pub)","*.pub")]
        )
        
        if (public_filename!=""):
            private_filename = fd.askopenfilename(
                initialdir = public_filename[0:(public_filename.rfind('/')+1)],
                title = "Select private key file",
                filetypes = [("Private key files (.pri)","*.pri")]
            )
            
            if (private_filename!=""):
                success = True 
            
        if (success):
            public_file = open(public_filename,"r")
            content_pub = public_file.read()
            
            e_pub = int(content_pub[0:(content_pub.find(' ')+1)])
            n_pub = int(content_pub[(content_pub.find(' ')+1):])
            
            public_file.close()
            
            private_file = open(private_filename,"r")
            content_pri = private_file.read()
            
            d_pri = int(content_pri[0:(content_pri.find(' ')+1)])
            n_pri = int(content_pri[(content_pri.find(' '))+1:])
            
            private_file.close()
            
            if (n_pub==n_pri):
                if (math.gcd(e_pub,d_pri)==1):
                    self.e_key_label["text"] = "e : " + str(e_pub)
                    self.d_key_label["text"] = "d : " + str(d_pri)
                    self.n_key_label["text"] = "n : " + str(n_pub)
                    #self.d_key["text"] = "d: " + str(d_pri)
                    #self.n_key["text"] = "n: " + str(n_pub)
                else:
                    self.AlertWindow("Sepertinya file key salah. Coba dicek lagi.")
            else:
                self.AlertWindow("Sepertinya file key salah. Coba dicek lagi.")
        return "break"
        
                
    def SaveEncryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            self.AlertWindow("Please choose a file")
        else:
            #encrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                # baca file per byte lalu simpan menjadi array of integer (byte)
                plaintext_byteintarray = OpenFileAsByteIntArray(self.file)
                
                key_byteintarray = StringToByteIntArray(key)
                
                # encrypt
                ciphertext_byteintarray = ModifiedRC4Encrypt(plaintext_byteintarray,key)
                
                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    # save hasil enkripsi per byte
                    output_file = open(filename, "wb")
                    
                    for byteint in ciphertext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                    
                    output_file.close()
        
    def SaveDecryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            self.AlertWindow("Please choose a file")
        else:
            # decrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                # baca file per byte lalu simpan menjadi array of integer (byte)
                ciphertext_byteintarray = OpenFileAsByteIntArray(self.file)
                
                key_byteintarray = StringToByteIntArray(key)
                
                # decrypt
                plaintext_byteintarray = ModifiedRC4Decrypt(ciphertext_byteintarray,key)

                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    # save hasil enkripsi per byte
                    output_file = open(filename, "wb")
                    
                    for byteint in plaintext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                    
                    output_file.close()
    
    def UnselectFile(self):
        self.file = ""
        self.file_label["text"] = "File : " + self.file
        
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()
