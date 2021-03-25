import math

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
    
def BlockByteIntArray(byteint_array,size):
    if (size==1):
        return byteint_array
    else:
        blocked_byteintarray = []
        i = 0
        while (i<len(byteint_array)):
            block = ""
            for j in range(size):
                if ((i+j)<len(byteint_array)):
                    if (byteint_array[i+j]<10):
                        block += "00" + str(byteint_array[i+j])
                    elif (byteint_array[i+j]<100):
                        block += "0" + str(byteint_array[i+j])
                    else:
                        block += str(byteint_array[i+j])
                else:
                    block += str(ord('/0'))
                
            i = i + size
            blocked_byteintarray.append(int(block))
            
        return blocked_byteintarray
        
def BlockCiphertext(ciphertext,n):
    # Input : ciphertext panjang dalam digit hexadecimal
    # Output : array ciphertext per blok sesuai 32 log n
    block_size = math,ceil(math.log(n,16))
    ciphertext_string = str(ciphertext)
    
    ciphertext_block = []
    i = 0
    while (i<len(ciphertext_block)):
        block = ""
        for j in range(block_size):
            if ((i+j)<len(ciphertext_string)):
                block += ciphertext_string[i+j]
        
        i = i + block_size
        ciphertext_block.append(int(block,16))

    return ciphertext_block
    
def RSAEncrypt(plaintext_byteintarray,e,n,size):
    # RSA Encrypt
    # Input :   plaintext_byteintarray (byte in array)
    #           key (e,n)
    #           block size
    # Output :  ciphertext string (in hex)

    plaintext_blocks = BlockByteIntArray(plaintext_byteintarray,size)
    ciphertext_blocksize = math.ceil(math.log(n,16))
    
    ciphertext_hexstr = ""
    for block in plaintext_blocks:
        cipher_block = (block**e)%n
        cipher_hex = str(hex(cipher_block))[2:]
        if (len(cipher_hex)<ciphertext_blocksize):
            leading_zero = "0" * (ciphertext_blocksize-len(cipher_hex))
            cipher_hex = leading_zero + cipher_hex
            
        ciphertext_hexstr += cipher_hex
    
    return ciphertext_hexstr
    
def RSADecrypt(ciphertext_hexstr,d,n):
    # RSA Decrypt
    # Input :   ciphertext_hexstr (string of hexadecimal)
    #           key (d,n)
    # Output :  plaintext (byte in array)

    ciphertext_blocks = BlockCiphertext(ciphertext_hexstr)
    
    plaintext = ""
    for block in ciphertext_blocks:
        plaintext_block = (int(block,16)**d)%n
        plaintext_blockstr = str(plaintext_block)
        if (len(plaintext_blockstr)%3!=0):
            leading_zero = "0" * (3-len(plaintext_blockstr)%3)
            plaintext_blockstr = leading_zero + plaintext_blockstr
            
        i = 0
        while (i<len(plaintext_blockstr)):
            num = plaintext_blockstr[i:i+3]
            plaintext += chr(int(num))
            i = i + 3
            
    return plaintext