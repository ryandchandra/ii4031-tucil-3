def StringToByteIntArray(string):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : string
    # Output : array of integer (byte) dari string
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array

def OpenFileAsByteIntArray(filename):
    # Membuka file dengan nama filename per byte lalu menyimpannya menjadi array of integer (byte)
    # Input : filename
    # Output : array of integer (byte) dari isi file
    
    # Buka file
    input_file = open(filename,"rb")
    
    # Baca isi file per byte hingga habis
    byteint_array = []
    byte = input_file.read(1)
    while (byte):
        # Ubah byte tersebut menjadi integer yang sesuai lalu masukkan ke array
        byteint = int.from_bytes(byte,byteorder='little')
        byteint_array.append(byteint)
        byte = input_file.read(1)
        
    # Tutup file
    input_file.close()
        
    return byteint_array

def ModifiedKey(key):
    # Create Modified key in Stream Cipher
    # Input : key (string any length)
    # Output : modified key in numbers (length >= 256)

    # Change key to numbers
    modified_key = StringToByteIntArray(key)

    # Modified key if length <256
    i = len(modified_key)
    while (i<256):
        if (i==1):
            modified_key.append((2*modified_key[i-1])%256)
        else:
            modified_key.append((modified_key[i-1]+modified_key[i-2])%256)
        i = len(modified_key)

    return modified_key

def ModifiedKSA(key):
    # Create Modified KSA in Stream Cipher
    # Input : key (string any length)
    # Output : larik S teracak (numbers 0-255)

    # Inisialisasi larik S
    larik_S = []
    for i in range(256):
        larik_S.append(i)

    # Pengacakan larik S
    # Modifikasi: larik_S[i] --> larik_S[K[i]]
    # Sehingga menghasilkan nilai j yang lebih acak
    K = ModifiedKey(key)
    j = 0
    for i in range(256):
        j = (j+larik_S[K[i]]+K[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]

    return larik_S

def PermutationEncrypt(byteintarray,block_length):
    # Melakukan permutasi lanjutan pada byteintarray
    # Permutasi yang dilakukan : 
    # 1. Membagi byteintarray menjadi blok-blok dengan panjang blocklength, kemudian masing-masing blok diberikan offset sesuai urutan blok
    #    Misal : blok 1 diberikan offset 1, blok 2 diberikan offset 2, dst
    # 2. Setiap pasangan 2 byte diswap. Jika jumlah byte ganjil, byte terakhir dibiarkan
    # Input : byteintarray (array of byte yang akan dipermutasi), block_length (panjang blok)
    # Output : array of integer (byte) yang sudah diubah
    
    modified_byteintarray = byteintarray
    array_length = len(byteintarray)
    
    # Berikan offset sesuai nomor blok
    for i in range(array_length):
        offset = i//block_length + 1
        modified_byteintarray[i] = (modified_byteintarray[i] + offset)%256

    # Lakukan swap untuk setiap pasangan 2 byte
    i = 0
    while (i<array_length):
        if (i!=array_length-1):
            modified_byteintarray[i], modified_byteintarray[i+1] = modified_byteintarray[i+1], modified_byteintarray[i]
            i = i + 2
        else:
            i = i + 1
    
    return modified_byteintarray
    
def PermutationDecrypt(byteintarray,block_length):
    # Mengembalikan efek permutasi yang dilakukan pada byteintarray
    # Langkah pengembalian :
    # 1. Swap setiap pasangan 2 byte. Jika jumlah byte ganjil, byte terakhir dibiarkan
    # 2. Membagi array hasil swap menjadi blok-blok dengan panjang blocklength, kemudian masing-masing blok dikurangi offset sesuai urutan blok
    #    Misal : blok 1 dikurangi offset 1, blok 2 dikurangi offset 2, dst
    # Input : byteintarray (array of byte yang sudah dipermutasi), block_length (panjang blok)
    # Output : array of integer (byte) yang benar
    
    modified_byteintarray = byteintarray
    array_length = len(byteintarray)
    
    # Lakukan swap untuk setiap pasangan 2 byte
    i = 0
    while (i<array_length):
        if (i!=array_length-1):
            modified_byteintarray[i], modified_byteintarray[i+1] = modified_byteintarray[i+1], modified_byteintarray[i]
            i = i + 2
        else:
            i = i + 1
    
    # Kurangi offset sesuai nomor blok
    for i in range(array_length):
        offset = i//block_length + 1
        modified_byteintarray[i] = (modified_byteintarray[i] - offset)%256
    
    return modified_byteintarray
    
def ModifiedRC4Encrypt(plaintext_byteintarray,key):
    # Create Normal PRGA Encrypt in Stream Cipher
    # Input :   plaintext_byteintarray (byte in array)
    #           key (string any length)
    # Output :  ciphertext (byte in array)

    # Generate key sesuai algoritma yang dimodifikasi
    larik_S = ModifiedKSA(key)
    i = 0
    j = 0
    ciphertext_byteintarray = []

    # PRGA
    # Catatan : Diadaptasi dari slide kuliah II4031 Kriptografi dan Koding yang berjudul "Stream Cipher" (2021) oleh Rinaldi Munir pada slide 31-32
    for idx in range(len(plaintext_byteintarray)):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        ciphertext_byteintarray.append(keystream^plaintext_byteintarray[idx])
    # Akhir dari bagian yang diadaptasi
    
    # Lakukan postprocessing lanjutan untuk permutasi
    ciphertext_byteintarray = PermutationEncrypt(ciphertext_byteintarray,len(key))
    
    return ciphertext_byteintarray
    
def ModifiedRC4Decrypt(ciphertext_byteintarray,key):
    # Create Normal PRGA Decrypt in Stream Cipher
    # Input :   ciphertext_byteintarray (byte in array)
    #           key (string any length)
    # Output :  plaintext (byte in array)

    # Generate key sesuai algoritma yang dimodifikasi
    larik_S = ModifiedKSA(key)
    i = 0
    j = 0
    plaintext_byteintarray = []

    # Kembalikan terlebih dahulu postprocessing permutasi yang dilakukan
    ciphertext_byteintarray = PermutationDecrypt(ciphertext_byteintarray,len(key))

    # PRGA
    # Catatan : Diadaptasi dari slide kuliah II4031 Kriptografi dan Koding yang berjudul "Stream Cipher" (2021) oleh Rinaldi Munir pada slide 33-34
    for idx in range(len(ciphertext_byteintarray)):
        i = (i+1)%256
        j = (j+larik_S[i])%256
        larik_S[i], larik_S[j] = larik_S[j], larik_S[i]
        temp = (larik_S[j] + larik_S[i])%256
        keystream = larik_S[temp]
        plaintext_byteintarray.append(keystream^ciphertext_byteintarray[idx])
    # Akhir dari bagian yang diadaptasi
            
    return plaintext_byteintarray