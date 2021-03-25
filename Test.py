# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from GenerateKeyLib import *
from random import randint
import tkinter.filedialog as fd
from RSALib import *

A = StringToByteIntArray('Aku Kamu Dia')
print(A)
B = RSAEncrypt(A, 107, 253, 1)
print (B)

C = HexStringToByteIntArray(B)
print (C)

D = ""
for byte in C:
    cipher_hex = str(hex(byte))[2:].upper()
    D = D + cipher_hex
print(D)

E = RSADecrypt(D,183,253) 
print(E)