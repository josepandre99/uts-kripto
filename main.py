from modes import *
from function import *



def readFile(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data.decode('iso8859-1')


def writeFile(filename, data):
    f = open(filename, "wb")
    bytearray = data.encode('iso8859-1')
    result = f.write(bytearray)
    if (result):
        print("Write file success")
    


if __name__ == "__main__":
    
    key = 'key12345key12345'
    
    plain_text = readFile('Test.txt')
    print(plain_text)
    
    
    m = Modes(plain_text, key)
    cipher = m.ecb_encrypt()
    print("Hasil Enkripsi:", cipher)

    m = Modes(cipher, key)
    plain = m.ecb_decrypt()
    print("hasil Dekripsi:", plain)
    
    writeFile('Output.txt', plain)