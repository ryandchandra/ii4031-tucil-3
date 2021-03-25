import tkinter as tk
import tkinter.scrolledtext as st

class FileHandlingWindow:
    def __init__(self,parent):
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title("Encrypt/Decrypt File")
        
        self.file = ""

        # Define elements
        self.file_label = tk.Label(master=self.window,text="File : " + self.file,width=50)
        self.file_label.grid(row=0,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        
        # Button list
        tk.Button(master=self.window,text="Choose File",width=20,command=self.ChooseFile).grid(row=3,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Encrypt and Save",width=20,command=self.SaveEncryptedFile).grid(row=4,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Decrypt and Save",width=20,command=self.SaveDecryptedFile).grid(row=5,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Unselect File",width=20,command=self.UnselectFile).grid(row=6,column=0,columnspan=2,pady=2)
        
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
