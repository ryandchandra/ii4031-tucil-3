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
        self.parent.columnconfigure([0,1,2,3],weight=1)
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
        self.role_frame.frame.grid(row=0,column=2,columnspan=2);
        
        #--- key frame ---#
        key_button_list = ["Generate Key","Alice Public Key","Alice Private Key","Clear Alice Key","Bob Public Key","Bob Private Key","Clear Bob Key"]
        self.key_frame = ButtonListFrame(
            title = "Key Management",
            labels = key_button_list,
            width = 25
        )
        self.key_frame.button_list[0].bind("<Button-1>",self.GenerateKey)
        self.key_frame.button_list[1].bind("<Button-1>",lambda event,type="public",subject="Alice": self.ChooseKeyFile(event,type,subject))
        self.key_frame.button_list[2].bind("<Button-1>",lambda event,type="private",subject="Alice": self.ChooseKeyFile(event,type,subject))
        self.key_frame.button_list[3].bind("<Button-1>",lambda event,subject="Alice": self.ClearKey(event,subject))
        self.key_frame.button_list[4].bind("<Button-1>",lambda event,type="public",subject="Bob": self.ChooseKeyFile(event,type,subject))
        self.key_frame.button_list[5].bind("<Button-1>",lambda event,type="private",subject="Bob": self.ChooseKeyFile(event,type,subject))
        self.key_frame.button_list[6].bind("<Button-1>",lambda event,subject="Bob": self.ClearKey(event,subject))
        self.key_frame.frame.grid(row=1,column=3,rowspan=3)
        
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
        
        self.button_frame.grid(row=2,column=0,columnspan=2)
        
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
        self.file_frame.frame.grid(row=1,column=2,rowspan=3)  
        
    def ChangeMode(self,event,role):
        # Mengganti role dari Alice menjadi Bob atau sebaliknya
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
                start_time = time.time()
                
                ciphertext_hexstr = RSAEncrypt(plaintext_byteintarray,e,n,1)

                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Insert into ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",ciphertext_hexstr)
                
                self.AlertWindow("Process finished in " + str(elapsed_time) + "s")
            
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
                start_time = time.time()
                
                plaintext_byteintarray = RSADecrypt(ciphertext,d,n)
                plaintext = bytes(plaintext_byteintarray)
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Insert into plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",plaintext)
                
                self.AlertWindow("Process finished in " + str(elapsed_time) + "s")
        
    def GenerateKey(self,event):
        # Membuka window baru untuk membuat key baru
        key_window = GenerateKeyWindow(self.parent)
        key_window.window.grab_set()
        
        return "break"
        
    def ChooseKeyFile(self,event,type,subject):
        if (type=="public"): # File public key
            public_filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select " + subject + " public key file",
                filetypes = [("Public key files (.pub)","*.pub")]
            )
            
            if (public_filename!=""):
                # Baca file
                public_file = open(public_filename,"r")
                content_pub = public_file.read()
                
                # Ambil nilai e dan n
                e_pub = int(content_pub[0:(content_pub.find(' ')+1)])
                n_pub = int(content_pub[(content_pub.find(' ')+1):])
                
                public_file.close()

                # Masukkan isi file
                if (subject=="Alice"): # Untuk Alice
                    if (self.Alice_n==-1 or self.Alice_d==-1): # Jika n Alice belum diset (key Alice belum diset), atau baru e dan n Alice yang diset, masukkan e dan n langsung
                        self.Alice_e = e_pub
                        self.Alice_n = n_pub
                        if (self.role=="Alice"):
                            self.Alice_frame.UpdateKey(e_pub,self.Alice_d,n_pub)
                        elif (self.role=="Bob"):
                            self.Alice_frame.UpdateKey(e_pub,"-1",n_pub)
                    elif (self.Alice_d!=-1 and self.Alice_n==n_pub): # Jika d dan n Alice sudah diset dan sesuai dengan n baru
                        if (math.gcd(e_pub,self.Alice_d)==1):
                            self.Alice_e = e_pub
                            self.Alice_n = n_pub
                            if (self.role=="Alice"):
                                self.Alice_frame.UpdateKey(e_pub,self.Alice_d,n_pub)
                            elif (self.role=="Bob"):
                                self.Alice_frame.UpdateKey(e_pub,"-1",n_pub)
                        else:
                            self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                    else:
                        self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                elif (subject=="Bob"):
                    if (self.Bob_n==-1 or self.Bob_d==-1):
                        self.Bob_e = e_pub
                        self.Bob_n = n_pub
                        if (self.role=="Alice"):
                            self.Bob_frame.UpdateKey(e_pub,"-1",n_pub)
                        elif (self.role=="Bob"):
                            self.Bob_frame.UpdateKey(e_pub,self.Bob_d,n_pub)
                    elif (self.Bob_d!=-1):
                        if (math.gcd(e_pub,self.Bob_d)==1):
                            self.Bob_e = e_pub
                            self.Bob_n = n_pub
                            if (self.role=="Alice"):
                                self.Bob_frame.UpdateKey(e_pub,"-1",n_pub)
                            elif (self.role=="Bob"):
                                self.Bob_frame.UpdateKey(e_pub,self.Bob_d,n_pub)
                        else:
                                self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                    else:
                        self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                            
        elif (type=="private"):
            private_filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select " + subject + " private key file",
                filetypes = [("Private key files (.pri)","*.pri")]
            )
            
            if (private_filename!=""):
                private_file = open(private_filename,"r")
                content_pri = private_file.read()
                
                d_pri = int(content_pri[0:(content_pri.find(' ')+1)])
                n_pri = int(content_pri[(content_pri.find(' ')+1):])
                
                private_file.close()
                
                if (subject=="Alice"):
                    if (self.Alice_n==-1 or self.Alice_e==-1): # Jika n Alice belum diset (key Alice belum diset), atau baru e dan n Alice yang diset, masukkan e dan n langsung
                        self.Alice_d = d_pri
                        self.Alice_n = n_pri
                        if (self.role=="Alice"):
                            self.Alice_frame.UpdateKey(self.Alice_e,d_pri,n_pri)
                        elif (self.role=="Bob"):
                            self.Alice_frame.UpdateKey(self.Alice_e,"-1",n_pri)
                    elif (self.Alice_e!=-1 and self.Alice_n==n_pri): # Jika d dan n Alice sudah diset dan sesuai dengan n baru
                        if (math.gcd(d_pri,self.Alice_e)==1):
                            self.Alice_d = d_pri
                            self.Alice_n = n_pri
                            if (self.role=="Alice"):
                                self.Alice_frame.UpdateKey(self.Alice_e,d_pri,n_pri)
                            elif (self.role=="Bob"):
                                self.Alice_frame.UpdateKey(self.Alice_e,"-1",n_pri)
                        else:
                            self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                    else:
                        self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                elif (subject=="Bob"):
                    if (self.Bob_n==-1 or self.Bob_e==-1): # Jika n Bob belum diset (key Bob belum diset), atau baru e dan n Bob yang diset, masukkan e dan n langsung
                        self.Bob_d = d_pri
                        self.Bob_n = n_pri
                        if (self.role=="Alice"):
                            self.Bob_frame.UpdateKey(self.Bob_e,"-1",n_pri)
                        elif (self.role=="Bob"):
                            self.Bob_frame.UpdateKey(self.Bob_e,d_pri,n_pri)
                    elif (self.Bob_e!=-1 and self.Bob_n==n_pri): # Jika d dan n Bob sudah diset dan sesuai dengan n baru
                        if (math.gcd(d_pri,self.Bob_e)==1):
                            self.Bob_d = d_pri
                            self.Bob_n = n_pri
                            if (self.role=="Alice"):
                                self.Bob_frame.UpdateKey(self.Bob_e,"-1",n_pri)
                            elif (self.role=="Bob"):
                                self.Bob_frame.UpdateKey(self.Bob_e,d_pri,n_pri)
                        else:
                            self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                    else:
                        self.AlertWindow("Ada kesalahan pada key. Silakan cek lagi.")
                            
        return "break"
        
    def ClearKey(self,event,subject):
        if (subject=="Alice"):
            self.Alice_e = -1
            self.Alice_d = -1
            self.Alice_n = -1
            self.Alice_frame.UpdateKey("-1","-1","-1")
        elif (subject=="Bob"):
            self.Bob_e = -1
            self.Bob_d = -1
            self.Bob_n = -1
            self.Bob_frame.UpdateKey("-1","-1","-1")
        
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