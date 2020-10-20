import math
import numpy as np
import random
from function import *

class BlockCipher:
    
    BLOCK_LENGTH = 128
    KEY_LENGTH = 128
    NUMBER_ITERATION = 16
    
    sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
    
    list_power_2 = [0, 1, 2, 4, 8, 16, 32, 64]
        
    def __init__(self, bit_plain_text, bit_key):
        self.bit_plain_text = bit_plain_text
        self.bit_key = bit_key
        if (len(bit_plain_text)%128 != 0):
            self.bit_plain_text = fix_size_multiple_128(self.bit_plain_text)[0]
        self.seed_key = self.count_seed(self.bit_key)
        
    def print_data(self):
        print("Plain text :", self.bit_plain_text)
        print("Key :", self.bit_key)
    
    
    
    # Jaringan feistel encrypt
    def encrypt(self):
        bit_plain_text = self.bit_plain_text
        
        left_bit = bit_plain_text[:self.BLOCK_LENGTH//2]
        right_bit = bit_plain_text[self.BLOCK_LENGTH//2:]
        
        for i in range (self.NUMBER_ITERATION):
            round_key = self.generate_round_key(self.bit_key, i)
            key_bit = convert_str_to_bit(round_key)
            temp_bit = left_bit
            left_bit = right_bit
            f_return = self.f_function(right_bit, key_bit)
            right_bit = xor_bit(temp_bit, f_return)
            
        
        temp_bit = left_bit
        left_bit = right_bit
        right_bit = temp_bit
        
        return left_bit + right_bit
    
    
    def decrypt(self):
        bit_plain_text = self.bit_plain_text
        
        left_bit = bit_plain_text[:self.BLOCK_LENGTH//2]
        right_bit = bit_plain_text[self.BLOCK_LENGTH//2:]
        
        # coba dekripsi
        for i in range (self.NUMBER_ITERATION):
            round_key = self.generate_round_key(self.bit_key, self.NUMBER_ITERATION-i-1)
            key_bit = convert_str_to_bit(round_key)
            temp_bit = left_bit
            left_bit = right_bit
            f_return = self.f_function(right_bit, key_bit)
            right_bit = xor_bit(temp_bit, f_return)
            
        temp_bit = left_bit
        left_bit = right_bit
        right_bit = temp_bit

        return left_bit + right_bit
        
            
    def count_seed(self, bit_key):
        str_key = convert_bit_to_str(bit_key)
        seed = 0
        for i in range(len(str_key)):
            seed += ord(str_key[i])
        return seed
        
    
    
    def generate_round_key(self, external_key, iter_number):
        random.seed(self.seed_key + iter_number)
        round_key = ''
        for _ in range(8):
            pos = random.randint(0, len(external_key)-1)
            round_key += external_key[pos]
        return round_key
    
    
    def f_function(self, right_bit, round_key_bit):
        temp = self.substitusi_bit(right_bit)   # apply substitusi bit
        temp = self.transpose_matrix(temp)    # apply transpose matrix
        temp = self.s_box_operation(temp)   # apply s-box
        temp = self.mod_operation(temp, round_key_bit)  # apply mod operation
        temp = xor_bit(temp, round_key_bit)    # XOR right_bit with round_key_bit
        return temp
        
        
    def transpose_matrix(self, bit_string):   # asumsi len(bit_string) = 64
        if len(bit_string) != 64:
            raise Exception()
        matrix = []
        for i in range(len(bit_string)//8):
            row = []
            for j in range(len(bit_string)//8):
                row.append(bit_string[i*8+j])
            matrix.append(row)
            
        matrix_trans = []
        for j in range(len(matrix[0])):
            row = []
            for i in range(len(matrix)):
                row.append(matrix[i][j])
            matrix_trans.append(row)        
            
        result = ''
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                result += matrix_trans[i][j]    
        
        # print("===================")
        # for i in range(8):
        #     for j in range(8):
        #         print(f"{matrix_trans[i][j]} ", end='')
        #     print("")
        
        return result


    def s_box_operation(self, bit_string):    # S-BOX Rijndael, input string bit, output string bit
        hex_string = convert_bit_to_hex(bit_string)
        new_bit_string = ''
        
        for i in range(len(hex_string)//2):
            new_bit_string += str('{0:08b}'.format(self.sbox[int(hex_string[i*2:i*2+2], 16)]))

        return new_bit_string
        
    
    def substitusi_bit(self, bit_string):  # bit pada posisi bukan perpangkatan 2 diubah, bit 0 --> 1, bit 1 --> 0
        bit_string_copy = ''
        for i in range(len(bit_string)):
            if i in self.list_power_2:
                bit_string_copy += bit_string[i]
            else:   # i not in self.list_power_2
                if (bit_string[i] == '1'):
                    bit_string_copy += '0'
                else:   # bit_string[i] == '0'
                    bit_string_copy += '1'
        return bit_string_copy
    

    def mod_operation(self, bit_string, round_key_bit):
        ord_round_key = int(round_key_bit, 2)
        
        new_bit_string = ''
        for i in range(len(bit_string)//8):
            new_bit_string += convert_str_to_bit(chr((int(bit_string[i*8:i*8+8], 2) * ord_round_key) % 255))
        
        return new_bit_string


    
if __name__ == "__main__":
    # enkripsi
    a = BlockCipher(convert_str_to_bit('abcdefghijklmnop'), convert_str_to_bit('key12345key12345'))
    a.print_data()
    cipher = a.encrypt()
    print(len(cipher))
    print("hasil enkripsi :", convert_bit_to_str(cipher))

    # dekripsi
    a = BlockCipher(cipher, convert_str_to_bit('key12345key12345'))
    plain = a.decrypt()
    print("hasil dekripsi :", convert_bit_to_str(plain))

