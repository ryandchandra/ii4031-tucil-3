# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from GenerateKeyLib import *
from random import randint
import tkinter.filedialog as fd
from RSALib import *

A = StringToByteIntArray('Aku Kamu Kita')
B = BlockByteIntArray(A,2)
print (A)
print (B)

    
