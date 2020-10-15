import block_cipher as bc
import random
from function import *


BLOCK_LENGTH = 128

class Modes:
    def __init__(self, plain_text, key):
        self.plain_text = plain_text
        self.key = key
        self.list_plain_text = split_string_into_list_of_length_16(plain_text)
        print("plain :", self.plain_text)
        print("key :", self.key)
        
    # ECB    
    def ecb_encrypt(self):
        result = ''
        for i in self.list_plain_text:
            f = bc.BlockCipher(i, self.key)
            result += f.encrypt()
        return result

    def ecb_decrypt(self):
        result = ''
        for i in self.list_plain_text:
            f = bc.BlockCipher(i, self.key)
            result += f.decrypt()
        return result
    
    
    # CBC
    def cbc_encrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''

        for i in self.list_plain_text:
            if index == 0:
                c = iv
            temp = xor_bit(fix_size_multiple_128(convert_str_to_bit(i))[0], convert_str_to_bit(c))        
            f = bc.BlockCipher(convert_bit_to_str(temp), self.key)
            c = f.encrypt()
            result += c
            index += 1
        
        return result

    def cbc_decrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''

        for i in self.list_plain_text:
            f = bc.BlockCipher(i, self.key)
            if index == 0:
                c = convert_str_to_bit(iv)
            p = f.decrypt()
            p = xor_bit(convert_str_to_bit(p), c)
            c = convert_str_to_bit(i)
            result += convert_bit_to_str(p)
            index += 1

        return result
    
    
## Test ECB
# enkripsi
ecb = Modes('abcdefghijklmnopa', 'key12345key12345')
cipher = ecb.ecb_encrypt()
print("Total enkripsi:", cipher)

# dekripsi
ecb = Modes(cipher, 'key12345key12345')
plain = ecb.ecb_decrypt()
print("Total dekripsi:", plain)

print("===========================================================")

## Test cbc
# enkripsi
cbc = Modes('abcdefghijklmnopa', 'key12345key12345')
cipher = cbc.cbc_encrypt()
print("Total enkripsi:", cipher)

# dekripsi
cbc = Modes(cipher, 'key12345key12345')
plain = cbc.cbc_decrypt()
print("Total dekripsi:", plain)


