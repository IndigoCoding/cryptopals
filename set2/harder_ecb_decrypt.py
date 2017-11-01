import aescbc
import os
import random
import time
from datetime import datetime
import math

def randomize():
	return os.urandom(16)

key = randomize()
prefix = os.urandom(random.randint(1,256))
plaintext = ""

def encryption_oracle(message, mystring):
	global key,prefix
	message = prefix + mystring + message.decode('base64')
	return aescbc.aes_128_encrypt_ecb(aescbc.pkcs7padding(message),key)

def detect_block_size(message):
	for blocksize in range(1,65):
		initvector = "1" * blocksize * 2
		result = encryption_oracle(message, initvector)
		chunks = list(map(''.join, zip(*[iter(result)]*blocksize)))
		if chunks[0] == chunks[1]:
			print "Block size is " + str(blocksize)
			return blocksize

	
def detect_mode(message, blocksize):
	initvector = "1" * blocksize * 4
	result = encryption_oracle(message, initvector)
	chunks = list(map(''.join, zip(*[iter(result)] * blocksize)))
	for chunk in chunks:
		if chunks.count(chunk) >= 3:
			print "ECB detected"
			return
	print "CBC detected"


def detect_prefix_length(message, blocksize):
	global prefix
	print "prefix length:", len(prefix)
	#time.sleep(1)
	initvector = "1" * blocksize * 2
	position = 1
	found = 0
	while True:
		result = encryption_oracle(message, initvector)
		chunks = list(map(''.join, zip(*[iter(result)] * blocksize)))
		for i in range(len(chunks) - 1):
			#print i
			#print repr(chunks[i]), repr(chunks[i+1])
			#time.sleep(0.1)
			if chunks[i] == chunks[i+1]: 
				position += i
				found = 1
				break
		if found == 1: break
		initvector += "1"
	return (position + 1) * blocksize - len(initvector)
	
def detect_message_length(message, blocksize, prefixsize):
	initlength = len(encryption_oracle(message, ""))
	for i in range(1,blocksize+1):
		if len(encryption_oracle(message,"1" * i)) != initlength:
			print "Message length is " + str(initlength - i - prefixsize)
			return initlength - i - prefixsize
		

def counting(message, char):
	count = 0
	for i in message:
		if i == char:
			count += 1
		else: break
	return count	
		
def detect_byte(message, blocksize, prefixsize, msglen, initvector):
	charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n-=[];'./,\!@#$%^&*()_+{}|:\"<>? "
	global plaintext
	container = int(math.ceil(float(msglen)/blocksize) * blocksize)
	if initvector == "":
		initvector = "a" * (container - 1 + prefixsize % blocksize) 
	result = encryption_oracle(message, initvector)
	for i in charset:
		fullvector = initvector + plaintext + i
		newresult = encryption_oracle(message, fullvector)
		if result[:(container + prefixsize + prefixsize % blocksize)] == newresult[:(container + prefixsize + prefixsize % blocksize)]:
			plaintext += i
			if (container - counting(initvector,"a")) ==  msglen: return plaintext
			detect_byte(message, blocksize, prefixsize, msglen, initvector[1:])
			return plaintext
			
if __name__ == "__main__":
	secret = open("simple_ecb_decrypt.txt","r").read()
	message = "".join(line.strip() for line in secret)
	print len(message.decode('base64'))	
	blocksize = 16
	detect_mode(message, blocksize)
	prefixsize = detect_prefix_length(message, blocksize)
	msglen = detect_message_length(message, blocksize, prefixsize)
	print detect_byte(message, blocksize, prefixsize, msglen, "")

	
	
