import codecs
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

asciiTextChars = list(range(97, 122)) + [32]

def hex2b64(hexstring):
    return b64encode(codecs.decode(hexstring, 'hex')).decode()

def xor2hex(hex1, hex2):
    return hex(int(hex1, 16) ^ int(hex2, 16))[2:]    

def bxor(s1, s2):
    return bytes([ x ^ y for (x, y) in zip(s1, s2)])    
    
def letterRatio(inputbytes):
    if not len(inputbytes):
        return 0
    r = sum([ord(x) in asciiTextChars for x in inputbytes])
    return r / len(inputbytes)

def isLetterString(inputbytes):
    return True if letterRatio(inputbytes) >= 0.7 else False

def breakSingleByteXor(ciphertext, outputKey = False):
    currentCandidate = ""
    currentKey = 0
    for i in range(2**8):
        keystream = (i.to_bytes(1, byteorder='big')) * len(ciphertext)
        message = bxor(ciphertext.encode(), keystream).decode("ISO-8859-1")
        if isLetterString(message) and letterRatio(message) >= letterRatio(currentCandidate):
            currentCandidate = message
            currentKey = i
    return currentKey if outputKey else currentCandidate

def repeatedXor(message, key):
    keystream = "".join([key[i % len(key)] for i in range(len(message))])
    return bxor(message.encode(), keystream.encode())

def hammingDistance(s1, s2):
    return bin(int.from_bytes(s1.encode(), 'big') ^ int.from_bytes(s2.encode(), 'big'))[2:].count('1')

def scoreKeySize(candidate_key_size, ciphertext):
    slice_size = 2*candidate_key_size
    nb_measurements = len(ciphertext) // slice_size - 1
    score = 0
    for i in range(nb_measurements):
        slice_1 = slice(i*slice_size, i*slice_size + candidate_key_size)
        slice_2 = slice(i*slice_size + candidate_key_size, i*slice_size + 2*candidate_key_size)
        score += hammingDistance(ciphertext[slice_1], ciphertext[slice_2])
    score /= candidate_key_size
    score /= nb_measurements
    return score    

def breakRepeatedXor(ciphertext):
    keySizeDict = dict()
    candidateKeySize = list()
    for keysize in range(2, 40):
        editDistance = scoreKeySize(keysize, ciphertext)
        keySizeDict[keysize] = editDistance
    for k in sorted(keySizeDict, key=keySizeDict.get):
        if len(candidateKeySize) < 3:
            candidateKeySize.append(k)
    for k in candidateKeySize:
        key = ""
        ciphertextByKey = ciphertext + "\x00" * (k - len(ciphertext) % k)
        cipherBlocks = [ciphertextByKey[i:i+k] for i in range(0, len(ciphertextByKey), k)]
        for i in range(k):
            key += chr(breakSingleByteXor("".join([b[i] for b in cipherBlocks]), True))
        plaintext = repeatedXor(ciphertext, key)
        if isLetterString(plaintext.decode('ISO-8859-1')):
            return plaintext.decode('ISO-8859-1')

def aesEcbDecrypt(ciphertext, key, encoding='utf-8'):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext.encode(encoding)), AES.block_size).decode()

def detectEcb(ciphertext, blocksize=AES.block_size):
    cipherBlocks = {}
    for i in range(0, len(ciphertext), blocksize):
        currentBlock = ciphertext[i:i + blocksize]
        if not cipherBlocks.get(currentBlock):
            cipherBlocks[currentBlock] = 1
        else:
            return True
    return False    

if __name__ == '__main__':
    # print(hex2b64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"))
    # print(xor2hex("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"))
    # print(breakSingleByteXor(codecs.decode("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736", "hex").decode()))
    # currentCandidate = ""
    # for line in open('singlecharxor.txt', 'r'):
    #     message = breakSingleByteXor(codecs.decode(line.strip(), 'hex').decode('ISO-8859-1'))
    #     if letterRatio(message) >= letterRatio(currentCandidate):
    #         currentCandidate = message
    # print(currentCandidate)     
    # print(codecs.encode(repeatedXor("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", "ICE"), 'hex'))
    # print(hammingDistance('this is a test', 'wokka wokka!!!'))
    # ciphertext = b64decode(open('repeatbytexor.txt','r').read()).decode()
    # print(breakRepeatedXor(ciphertext))

    # key = "YELLOW SUBMARINE"
    # message = ""
    # for line in open('aesecb.txt', 'r'):
    #     message += line.strip()
    # print(aesEcbDecrypt(b64decode(message).decode('ISO-8859-1'), key, 'ISO-8859-1'))

    for line in open('detectecb.txt', 'r'):
        if detectEcb(line.strip()):
            print(line)
    pass