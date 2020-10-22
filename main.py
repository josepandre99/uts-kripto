from modes import *
from function import *
import time


def readFile(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data.decode('iso8859-1')


def writeFile(filename, data):
    f = open(filename, "wb")
    bytearray = data.encode('iso8859-1')
    result = f.write(bytearray)
    f.close()
    if (result):
        print("Write file success")
        

def writeFileText(filename, data):
    f = open(filename, "w+", encoding="utf-8")
    result = f.write(data)
    f.close()
    if (result):
        print("Write file success")
    


if __name__ == "__main__":
    
    key = 'key12345key12345'

    # Text File    
    plain_text = readFile('test/test-text.txt')
    # print(plain_text)
    
    plain_text1 = readFile('test/test-text1.txt')
    # print(plain_text1)
    

    # Mode ECB
    ## enkripsi
    start = time.time()
    m = Modes(plain_text, key)
    cipher = m.ecb_encrypt()
    end = time.time()
    print(end - start)
    writeFileText('test/output/cipher-ECB.txt', cipher)

    ## dekripsi
    start = time.time()
    m = Modes(cipher, key)
    plain = m.ecb_decrypt()
    end = time.time()
    print(end - start)
    writeFile('test/output/plain-ECB.txt', plain)
    
    
    # Mode CBC
    ## enkripsi
    start = time.time()
    m = Modes(plain_text, key)
    cipher = m.cbc_encrypt()
    end = time.time()
    print(end - start)
    writeFileText('test/output/cipher-CBC.txt', cipher)

    ## dekripsi
    start = time.time()
    m = Modes(cipher, key)
    plain = m.cbc_decrypt()
    end = time.time()
    print(end - start)
    writeFile('test/output/plain-CBC.txt', plain)
    
    
    # Mode Counter
    ## enkripsi
    start = time.time()
    m = Modes(plain_text, key)
    cipher = m.counter_encrypt()
    end = time.time()
    print(end - start)
    writeFileText('test/output/cipher-Counter.txt', cipher)


    # ## enkripsi1
    # start = time.time()
    # m1 = Modes(plain_text1, key)
    # cipher = m1.counter_encrypt()
    # end = time.time()
    # print(end - start)
    # writeFileText('test/output/cipher-Counter1.txt', cipher)


    ## dekripsi
    start = time.time()
    m = Modes(cipher, key)
    plain = m.counter_decrypt()
    end = time.time()
    print(end - start)
    writeFile('test/output/plain-Counter.txt', plain)
    

    # print("============================================================= Batas =============================================================")
    

    # # Image File
    # plain_text = readFile('test/test-image.png')
    

    # # Mode ECB
    # ## enkripsi
    # start = time.time()
    # m = Modes(plain_text, key)
    # cipher = m.ecb_encrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/cipher-ECB.png', cipher)

    # ## dekripsi
    # start = time.time()
    # m = Modes(cipher, key)
    # plain = m.ecb_decrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/plain-ECB.png', plain)
    
    
    # # Mode CBC
    # ## enkripsi
    # start = time.time()
    # m = Modes(plain_text, key)
    # cipher = m.cbc_encrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/cipher-CBC.png', cipher)

    # ## dekripsi
    # start = time.time()
    # m = Modes(cipher, key)
    # plain = m.cbc_decrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/plain-CBC.png', plain)
    
    
    # # Mode Counter
    # ## enkripsi
    # start = time.time()
    # m = Modes(plain_text, key)
    # cipher = m.counter_encrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/cipher-Counter.png', cipher)

    # ## dekripsi
    # start = time.time()
    # m = Modes(cipher, key)
    # plain = m.counter_decrypt()
    # end = time.time()
    # print(end - start)
    # writeFile('test/output/plain-Counter.png', plain)