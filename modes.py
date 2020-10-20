import block_cipher as bc
import random
from function import *


BLOCK_LENGTH = 128

class Modes:
    def __init__(self, plain_text, key):
        self.plain_text = plain_text
        self.key = key
        
        self.bit_plain_text = convert_str_to_bit(plain_text)
        self.bit_key = convert_str_to_bit(key)
        
        # print(len(self.bit_plain_text))
        
        self.list_bit_plain_text = split_string_into_list_of_length_n(self.bit_plain_text, 128)
        
        # print(self.list_bit_plain_text)
        # print("plain :", self.plain_text)
        # print("key :", self.key)
        
        
    # ECB    
    def ecb_encrypt(self):
        result = ''
        
        for i in self.list_bit_plain_text:
            f = bc.BlockCipher(i, self.bit_key)
            result += f.encrypt()
            
        return convert_bit_to_str(result)


    def ecb_decrypt(self):
        result = ''
        
        for i in self.list_bit_plain_text:
            f = bc.BlockCipher(i, self.bit_key)
            result += f.decrypt()
            
        return convert_bit_to_str(result)
    
    
    # CBC
    def cbc_encrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''
        
        for i in self.list_bit_plain_text:
            if index == 0:
                c = convert_str_to_bit(iv)
            p = xor_bit(fix_size_multiple_128(i)[0], c)        
            f = bc.BlockCipher(p, self.bit_key)
            c = f.encrypt()
            result += c
            index += 1
            
        return convert_bit_to_str(result)


    def cbc_decrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''
        
        for i in self.list_bit_plain_text:
            f = bc.BlockCipher(i, self.bit_key)
            if index == 0:
                c = convert_str_to_bit(iv)
            p = f.decrypt()
            p = xor_bit(p, c)
            c = i
            result += p
            index += 1
            
        return convert_bit_to_str(result)
    
    
    # Counter Mode
    def counter_encrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''
        counter = convert_str_to_bit(iv)
        
        for i in self.list_bit_plain_text:
            f = bc.BlockCipher(counter, self.bit_key)
            m = f.encrypt()
            c = xor_bit(m, fix_size_multiple_128(i)[0])
            result += c
            counter = bin(int(counter, 2) + 1)[2:].zfill(128)
            index += 1
            
        return convert_bit_to_str(result)


    def counter_decrypt(self):
        iv = 'masterencryption'
        index = 0
        result = ''
        counter = convert_str_to_bit(iv)
        
        for i in self.list_bit_plain_text:
            f = bc.BlockCipher(counter, self.bit_key)
            m = f.encrypt()
            c = xor_bit(m, fix_size_multiple_128(i)[0])
            result += c
            counter = bin(int(counter, 2) + 1)[2:].zfill(128)
            index += 1
            
        return convert_bit_to_str(result)
        
    
    # # CFB Mode
    # def cfb_encrypt(self):
    #     n = 1 #size of unit in bytes (sementara cuma bisa untuk 1 byte)
    #     iv = 'masterencryption'
    #     index = 0
    #     result = ''
    #     list_bitplain = split_string_into_list_of_length_n(self.bit_plain_text, (n*8))

    #     for i in list_bitplain:
    #         if index == 0:
    #             x = convert_str_to_bit(iv)
    #         f = bc.BlockCipher(x, self.bit_key)
    #         c = xor_bit(i, f.encrypt()[:n*8])
    #         result += c
    #         x = x[:(n*8)] + c
    #         index += 1
    #     print(result)
    #     return convert_bit_to_str(result)


    # def cfb_decrypt(self):
    #     n = 1 #size of unit in bytes
    #     iv = 'masterencryption'
    #     index = 0
    #     result = ''
    #     list_bitplain = split_string_into_list_of_length_n(self.bit_plain_text, (n*8))
        
    #     for i in list_bitplain:
    #         if index == 0:
    #             x = convert_str_to_bit(iv)
    #         f = bc.BlockCipher(x, self.bit_key)
    #         c = xor_bit(i, f.decrypt()[:n*8])
    #         result += c
    #         x = x[:(n*8)] + i
    #         index += 1
    #     print(result)
    #     return convert_bit_to_str(result)
    
    
    # # OFB Mode
    # def ofb_encrypt(self):
    #     n = 1 #size of unit in bytes (sementara cuma bisa untuk 1 byte)
    #     iv = 'masterencryption'
    #     index = 0
    #     result = ''

    #     for i in self.plain_text:
    #         if index == 0:
    #             x = iv
    #         print(f"plain {index} :", self.plain_text, "len x :", len(x))
    #         print("x :", x)
    #         f = bc.BlockCipher(x, self.key)
    #         print("f_encrypt :", f.encrypt(), "awal :", f.encrypt()[0], "bit :", bin(ord(f.encrypt()[0])))
    #         print("a :", convert_str_to_bit(i))
    #         print("b :", convert_str_to_bit(f.encrypt()[0]))
    #         c = xor_bit(convert_str_to_bit(i), convert_str_to_bit(f.encrypt()[0]).zfill(n*8))
    #         print("hasil :", c, "ascii :", convert_bit_to_str(c))
    #         result += c
    #         x = x[n:] + f.encrypt()[0]
    #         print("resultnya :", convert_bit_to_str(result), "lennya :", len(result))
    #         print("="*130)
    #         index += 1
        
    #     result = convert_bit_to_str(result)
    #     return result

    # def ofb_decrypt(self):
    #     n = 1 #size of unit in bytes
    #     iv = 'masterencryption'
    #     index = 0
    #     result = ''

    #     for i in self.plain_text:
    #         if index == 0:
    #             x = iv
    #         f = bc.BlockCipher(x, self.key)
    #         c = xor_bit(convert_str_to_bit(i), convert_str_to_bit(f.decrypt()[0]).zfill(n*8))
    #         result += c
    #         x = x[n:] + f.decrypt()[0]
    #         index += 1

    #     result = convert_bit_to_str(result)
    #     return result
    
    
    
    
''' =================================================== Testing =================================================== ''' 
# panjang iv = 16 karakter

if __name__ == "__main__":
        
    plain_text = 'abcdefghijklmnopa'
    key = 'key12345key12345'
        
    # # Test ECB
    # # enkripsi
    # ecb = Modes(plain_text, key)
    # cipher = ecb.ecb_encrypt()
    # print("Hasil enkripsi:", cipher)

    # # dekripsi
    # ecb = Modes(cipher, key)
    # plain = ecb.ecb_decrypt()
    # print("Hasil dekripsi:", plain)

    # print("===========================================================")

    ## Test CBC
    # # enkripsi
    # cbc = Modes(plain_text, key)
    # cipher = cbc.cbc_encrypt()
    # print("Hasil enkripsi:", cipher)

    # # dekripsi
    # cbc = Modes(cipher, key)
    # plain = cbc.cbc_decrypt()
    # print("Hasil dekripsi:", plain)

    # print("===========================================================")

    # Test Counter Mode
    # enkripsi
    counter = Modes(plain_text, key)
    cipher = counter.counter_encrypt()
    print("Hasil enkripsi:", cipher)

    # dekripsi
    counter = Modes(cipher, key)
    plain = counter.counter_decrypt()
    print("Hasil dekripsi:", plain)

    # print("===========================================================")

    # # Test CFB Mode
    # # enkripsi
    # cfb = Modes(plain_text, key)
    # cipher = cfb.cfb_encrypt()
    # print("Hasil enkripsi:", cipher)

    # # dekripsi
    # cfb = Modes(cipher, key)
    # plain = cfb.cfb_decrypt()
    # print("Hasil dekripsi:", plain)


    # print("===========================================================")

    ## Test OFB Mode
    # # enkripsi
    # ofb = Modes(plain, key)
    # cipher = ofb.ofb_encrypt()
    # print("Hasil enkripsi:", len(cipher))

    # # dekripsi
    # ofb = Modes(cipher, key)
    # plain = ofb.ofb_decrypt()
    # print("Hasil dekripsi:", plain)
