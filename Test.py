# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from GenerateKeyLib import *

p = 3556
q = 752

p = ValidationPrime(p)
q = ValidationPrime(q)

print (p)
print (q)

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