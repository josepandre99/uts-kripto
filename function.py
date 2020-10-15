BLOCK_LENGTH = 128

def convert_str_to_bit(string_text):
    bit_plain_text = ''
    for char in string_text:
        bit_plain_text += str('{0:08b}'.format(ord(char)))
    return bit_plain_text
    
    
def convert_bit_to_str(bitarray):
    string = ''
    for i in range (0, len(bitarray)//8):
        string += chr(int(bitarray[i*8:i*8+8], 2))
    return string


def convert_bit_to_hex(bitarray):
    str_hex = ''
    for i in range(len(bitarray)//4):
        str_hex += hex(int(bitarray[i*4:i*4+4], 2))[2:]
    
    return str_hex


def xor_bit(a, b):    # length a = b
    temp = ''
    for i in range(len(a)):
        if (a[i] == b[i]):
            temp += '0'
        else:
            temp += '1'
    return temp
    
    
def split_string_into_list_of_length_n(string, n):
    if (len(string) % n) != 0: 
        raise Exception()
    return [string[i:i + n] for i in range(0, len(string), n)]


def fix_size_multiple_128(bit_plain): 
    check = False
    if len(bit_plain) % 128 != 0:
        lack = int((128 - (len(bit_plain)%128)) / 8)
        for i in range(lack):
            bit_plain += '{0:08b}'.format(lack)
    else:
        check = True
        for i in range(16):
            bit_plain += '{0:08b}'.format(8)
    bit_plain_arr = split_string_into_list_of_length_n(bit_plain, 128)
    if (check):
        bit_plain_arr = bit_plain_arr[:-1]
    return bit_plain_arr


def split_string_into_list_of_length_16(string):
    n = 16
    return [string[i:i + n] for i in range(0, len(string), n)]