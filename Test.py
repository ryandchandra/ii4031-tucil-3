# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from GenerateKeyLib import *
from random import randint

p = 36
q = 64

p = ValidationPrime(p)
q = ValidationPrime(q)

print (p)
print (q)


n = p*q
toitent_euler = (p-1)*(q-1)
e = toitent_euler
while (e >= toitent_euler):
    e = randint (2, toitent_euler)
    e = ValidationPrime(e)

print (toitent_euler)
print (e)

found = 0
k = 1
while not(found):
    d = (1+k*toitent_euler)/e
    if ((e*int(d))%toitent_euler == 1):
        found = 1    
    k = k+1

print(d)