# Dimodifikasi dari program pada tugas sebelumnya

import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import math

from Components import *
from FileHandlingWindow import *
from GenerateKeyWindow import *

from RSALib import *

class GUI:
    def __init__(self,parent):
        #--- init ---#
        self.parent = parent
        self.parent.title("Kriptografi RSA")
        
        #--- role ---#
        self.role = "Alice"
        
        #--- define grid ---#
        self.parent.columnconfigure([0,1,2],weight=1)
        self.parent.rowconfigure([0,1,2,3],weight=1,minsize=100)
        
        #--- Alice frame ---#
        self.Alice_e = -1
        self.Alice_d = -1
        self.Alice_n = -1
        self.Alice_frame = SubjectFrame("Alice (You)")
        self.Alice_frame.frame.grid(row=0,column=0)
        
        #--- Bob frame ---#
        self.Bob_e = -1
        self.Bob_d = -1
        self.Bob_n = -1
        self.Bob_frame = SubjectFrame("Bob")
        self.Bob_frame.frame.grid(row=0,column=1)
        
        #--- role frame ---#
        role_list = ["Alice","Bob"]
        self.role_frame = ButtonListFrame(
            title = "Choose your Role",
            labels = role_list,
            width = 25
        )
        self.role_frame.button_list[0].bind("<Button-1>",lambda event,role="Alice": self.ChangeMode(event,role))
        self.role_frame.button_list[1].bind("<Button-1>",lambda event,role="Bob": self.ChangeMode(event,role))
        self.role_frame.button_list[0]["state"] = tk.DISABLED
        self.role_frame.frame.grid(row=0,column=2);
        
        #--- key frame ---#
        key_button_list = ["Generate Key","Choose Key for Alice","Choose Key for Bob"]
        self.key_frame = ButtonListFrame(
            title = "Key Management",
            labels = key_button_list,
            width = 25
        )
        self.key_frame.button_list[0].bind("<Button-1>",self.GenerateKey)
        self.key_frame.button_list[1].bind("<Button-1>",lambda event,subject="Alice": self.ChooseKeyFile(event,subject))
        self.key_frame.button_list[2].bind("<Button-1>",lambda event,subject="Bob": self.ChooseKeyFile(event,subject))
        self.key_frame.frame.grid(row=1,column=2)
        
        #--- plaintext ---#
        self.plaintext = TextFrame(
            title="Plaintext",
            width=60,
            height=5
        )
        self.plaintext.frame.grid(row=1,column=0,columnspan=2)
        
        #--- button frame ---#
        self.button_frame = tk.Frame()
        
        #--- encrypt button ---#
        self.encrypt_button = tk.Button(master=self.button_frame,text="Encrypt (as Alice) and Send (to Bob)",command=self.Encrypt,width=32)
        self.encrypt_button.pack(padx=2,pady=2)
        #self.encrypt_button.grid(row=2,column=0,padx=10,pady=10)

        #--- decrypt button ---#
        self.decrypt_button = tk.Button(master=self.button_frame,text="Receive (from Bob) and Decrypt (as Alice)",command=self.Decrypt,width=32)
        #self.decrypt_button.grid(row=2,column=1,padx=10,pady=10)
        self.decrypt_button.pack(padx=2,pady=2)
        
        self.button_frame.grid(row=2,column=0)
        
        #--- block size frame ---#
        self.block_size_frame = tk.Frame()
        
        self.block_size_label = tk.Label(master=self.block_size_frame,text="Block size (in bytes)")
        self.block_size_label.pack()
        
        self.block_size_entry = tk.Entry(master=self.block_size_frame)
        self.block_size_entry.pack()
        
        self.block_size_alert = tk.Label(master=self.block_size_frame,text="less than n in bytes")
        self.block_size_alert.pack()
        
        self.block_size_info = tk.Label(master=self.block_size_frame,text="default : 1")
        self.block_size_info.pack()
        
        self.block_size_frame.grid(row=2,column=1)
        
        #--- ciphertext ---#
        self.ciphertext = TextFrame(
            title="Ciphertext",
            width=60,
            height=5
        )
        self.ciphertext.frame.grid(row=3,column=0,columnspan=2)
        
        #--- file frame ---#
        file_method_list = ["Open Plaintext from File","Open Ciphertext from File","Save Plaintext to File","Save Ciphertext to File","Encrypt/Decrypt File"]
        self.file_frame = ButtonListFrame(
            title = "File",
            labels = file_method_list,
            width = 25
        )
        self.file_frame.button_list[0].bind("<Button-1>",lambda event,text="plaintext": self.OpenFileText(event,text))
        self.file_frame.button_list[1].bind("<Button-1>",lambda event,text="ciphertext": self.OpenFileText(event,text))
        self.file_frame.button_list[2].bind("<Button-1>",lambda event,text="plaintext": self.SaveFileText(event,text))
        self.file_frame.button_list[3].bind("<Button-1>",lambda event,text="ciphertext": self.SaveFileText(event,text))
        self.file_frame.button_list[4].bind("<Button-1>",self.EncryptDecryptFileWindow)
        self.file_frame.frame.grid(row=2,column=2,rowspan=2)  
        
    def ChangeMode(self,event,role):
        if (self.role==role):
            pass
        else:
            if (role=="Alice"):
                self.role = role
                self.role_frame.button_list[0]["state"] = tk.DISABLED
                self.role_frame.button_list[1]["state"] = tk.NORMAL
                self.Alice_frame.title_label["text"] = "Alice (You)"
                self.Bob_frame.title_label["text"] = "Bob"
                self.Bob_frame.d_key["text"] = "d: -"
                self.Alice_frame.d_key["text"] = "d: " + str(self.Alice_d)
                self.encrypt_button["text"] = "Encrypt (as Alice) and Send (to Bob)"
                self.decrypt_button["text"] = "Receive (from Bob) and Decrypt (as Alice)"
            elif (role=="Bob"):
                self.role = role
                self.role_frame.button_list[0]["state"] = tk.NORMAL
                self.role_frame.button_list[1]["state"] = tk.DISABLED
                self.Alice_frame.title_label["text"] = "Alice"
                self.Bob_frame.title_label["text"] = "Bob (You)"
                self.Alice_frame.d_key["text"] = "d: -"
                self.Bob_frame.d_key["text"] = "d: " + str(self.Bob_d)
                self.encrypt_button["text"] = "Encrypt (as Bob) and Send (to Alice)"
                self.decrypt_button["text"] = "Receive (from Alice) and Decrypt (as Bob)"
                
    def Encrypt(self):
        # Event handler when encrypt button is pressed
        # Encrypt plaintext and key
        
        # Take the plaintext and key from the field
        plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
        block_size = self.block_size_entry.get()
            
        # Check for validity
        if (len(plaintext)==0): # Empty plaintext
            self.AlertWindow("Please insert plaintext")
        else:
            plaintext_byteintarray = StringToByteIntArray(plaintext)
                
            # Encrypt
            if (self.role=="Alice"):
                e = self.Bob_e
                n = self.Bob_n
            elif (self.role=="Bob"):
                e = self.Alice_e
                n = self.Alice_n
                    
            if (e==-1 or n==-1):
                self.AlertWindow("Please choose key first")
            else:
                if (len(block_size)==0):
                    block_size = 1
                elif (int(block_size)<math.log(n,16)):
                    self.AlertWindow("Block size is too big. Please choose block size less than n")
                else:
                    block_size = int(block_size)
                    
                ciphertext_hexstr = RSAEncrypt(plaintext_byteintarray,e,n,block_size)
                
                # Insert into ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",ciphertext_hexstr)
            
    def Decrypt(self):
        # Event handler when decrypt button is pressed
        # Decrypt ciphertext and key
        
        # Take the ciphertext and key from the field
        ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]

        # Check for validity
        if (len(ciphertext)==0): # Empty ciphertext
            self.AlertWindow("Please insert ciphertext")
        else:
            if (self.role=="Alice"):
                d = self.Alice_d
                n = self.Alice_n
            elif (self.role=="Bob"):
                d = self.Bob_d
                n = self.Bob_n
            
            if (d==-1 or n==-1):
                self.AlertWindow("Please choose key for "+self.role)
            else:            
                # Decrypt
                plaintext_byteintarray = RSADecrypt(ciphertext,d,n)
                plaintext = bytes(plaintext_byteintarray)
                
                # Insert into plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",plaintext)
        
    def GenerateKey(self,event):
        key_window = GenerateKeyWindow(self.parent)
        key_window.window.grab_set()
        
        return "break"
        
    def ChooseKeyFile(self,event,subject):
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
                    if (subject=="Alice"):
                        self.Alice_e = e_pub
                        self.Alice_d = d_pri
                        self.Alice_n = n_pub
                        if (self.role=="Alice"):
                            self.Alice_frame.UpdateKey(e_pub,d_pri,n_pub)
                        elif (self.role=="Bob"):
                            self.Alice_frame.UpdateKey(e_pub,"-",n_pub)
                    elif (subject=="Bob"):
                        self.Bob_e = e_pub
                        self.Bob_d = d_pri
                        self.Bob_n = n_pub
                        if (self.role=="Alice"):
                            self.Bob_frame.UpdateKey(e_pub,"-",n_pub)
                        elif (self.role=="Bob"):
                            self.Bob_frame.UpdateKey(e_pub,d_pri,n_pub)
                else:
                    self.AlertWindow("Sepertinya file key salah. Coba dicek lagi.")
            else:
                self.AlertWindow("Sepertinya file key salah. Coba dicek lagi.")
        return "break"
        
    def OpenFileText(self,event,text):
        # Open file using open file dialog
        
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If filename is chosen
            content = OpenFileAsByteIntArray(filename)
            content_bytes = bytes(content)
            
            if (text=="plaintext"): # For plaintext, insert to plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",content_bytes)
            elif (text=="ciphertext"): # For ciphertext, insert to ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",content_bytes)
        
        return "break"
        
    def SaveFileText(self,event,text):
        # Save file using save file dialog
        
        # Take filename
        filename = fd.asksaveasfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")],
            defaultextension = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If file name is chosen
            file = open(filename,"wb")
            if (text=="plaintext"): # For plaintext, insert the plaintext
                plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
                plaintext_byteintarray = StringToByteIntArray(plaintext)
                for byteint in plaintext_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
            elif (text=="ciphertext"): # For ciphertext, insert the ciphertext
                ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]
                ciphertext_byteintarray = StringToByteIntArray(ciphertext)
                for byteint in ciphertext_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
                
            file.close()
        
        return "break"
        
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()
        
    def EncryptDecryptFileWindow(self,event):
        # Create new window for file encrypt/decrypt
        # Components : label, key entry, and buttons
        file_window = FileHandlingWindow(self.parent)
        file_window.window.grab_set()
        
        return "break"