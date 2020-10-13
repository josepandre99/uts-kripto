import math
import numpy as np

class block_cipher:
    
    block_length = 128
    key_length = 128
    iteration = 16
    
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
        
    def __init__(self, plain_text, key):
        self.plain_text = plain_text
        self.key = key 
        self.bit_plain_text = self.convert_str_to_bit(self.plain_text)
        
        
    def print_data(self):
        print("Plain text :", self.plain_text)
        print("Key :", self.key)
    
    
    def convert_str_to_bit(self, string_text):
        bit_plain_text = ''
        for char in string_text:
            bit_plain_text += str('{0:08b}'.format(ord(char)))
        # print(bit_plain_text)
        return bit_plain_text
    
    
    def convert_bit_to_char(self, bitarray):
        string = ''
        for i in range (0, len(bitarray)//8):
            string += chr(int(bitarray[i*8:i*8+8], 2))
        return string
    
    
    def convert_bit_to_hex(self, bitarray):
        str_hex = ''
        for i in range(len(bitarray)//4):
            str_hex += hex(int(bitarray[i*4:i*4+4], 2))[2:]
        
        return str_hex

    
    def xor_bit(self, a, b):
        temp = ''
        for i in range(len(a)):
            if (a[i] == b[i]):
                temp += '0'
            else:
                temp += '1'
        return temp
    
    
    # Jaringan Feistel
    def feistel(self, bit_plain_text):
        left_bit = bit_plain_text[:self.block_length//2]
        right_bit = bit_plain_text[self.block_length//2:]
        
        key_bit = self.convert_str_to_bit(self.key) # Asumsi semua internal key = eksternal key
        # print("key bit : ", key_bit)
        
        print("Awal       : ", self.convert_bit_to_char(left_bit + right_bit))
        
        for i in range (self.iteration):
            temp_bit = left_bit
            left_bit = right_bit
            f_return = self.f_function(right_bit, key_bit)
            right_bit = self.xor_bit(temp_bit, f_return)
            
            # print(f"left bit  {i} : ", self.convert_bit_to_char(left_bit))
            # print(f"right bit {i} : ", self.convert_bit_to_char(right_bit))
        
        temp_bit = left_bit
        left_bit = right_bit
        right_bit = temp_bit
        print("Hasil      : ", self.convert_bit_to_char(left_bit + right_bit))
        


        # coba dekripsi        
        for i in range (self.iteration):
            temp_bit = left_bit
            left_bit = right_bit
            f_return = self.f_function(right_bit, key_bit)
            right_bit = self.xor_bit(temp_bit, f_return)
            
        temp_bit = left_bit
        left_bit = right_bit
        right_bit = temp_bit
        print("Hasil Lagi : ", self.convert_bit_to_char(left_bit + right_bit))
        
        
        return left_bit + right_bit
    
            
    def f_function(self, right_bit, internal_key_bit):
        temp = self.xor_bit(right_bit, internal_key_bit)    # XOR right_bit with internal_key_bit
        temp = self.transpose_matrix(temp)    # apply transpose matrix
        temp = self.s_box_operation(temp)   # apply s-box
        return temp
        
        
    def transpose_matrix(self, bit_string):   # asumsi len(bit_string) = 64
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
        hex_string = self.convert_bit_to_hex(bit_string)
        new_bit_string = ''
        
        for i in range(len(hex_string)//2):
            new_bit_string += str('{0:08b}'.format(self.sbox[int(hex_string[i*2:i*2+2], 16)]))

        return new_bit_string
        
        

a = block_cipher('abcdefghijklmnop', 'key12345')
a.print_data()

# print(a.convert_str_to_bit())
cipher = a.feistel(a.convert_str_to_bit(a.plain_text))
# print(cipher)

a.s_box_operation(a.convert_str_to_bit(a.plain_text))

# print(a.convert_bit_to_hex(bin(a.sbox[int("23", 16)])))
# print(bin(0x26))
# print(a.convert_bit_to_hex('100110'))

