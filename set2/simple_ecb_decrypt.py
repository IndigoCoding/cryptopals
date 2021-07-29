import aescbc
import os
import random
import time
from datetime import datetime
import math

def randomize():
	return os.urandom(16)

key = randomize()
plaintext = ""

def encryption_oracle(message, mystring):
	global key
	message = mystring + message.decode('base64')
	return aescbc.aes_128_encrypt_ecb(aescbc.pkcs7padding(message),key)

def detect_block_size(message):
	for blocksize in range(1,65):
		initvector = "1" * blocksize * 2
		result = encryption_oracle(message, initvector)
		chunks = list(map(''.join, zip(*[iter(result)]*blocksize)))
		if chunks[0] == chunks[1]:
			print ("Block size is " + str(blocksize))
			return blocksize

	
def detect_mode(message, blocksize):
	initvector = "1" * blocksize * 4
	result = encryption_oracle(message, initvector)
	chunks = list(map(''.join, zip(*[iter(result)] * blocksize)))
	for chunk in chunks:
		if chunks.count(chunk) >= 3:
			print ("ECB detected")
			return
	print ("CBC detected")

def detect_message_length(message, blocksize):
	initlength = len(encryption_oracle(message, ""))
	for i in range(1,blocksize+1):
		if len(encryption_oracle(message,"1" * i)) != initlength:
			print ("Message length is " + str(initlength - i))
			return initlength - i
		

def counting(message, char):
	count = 0
	for i in message:
		if i == char:
			count += 1
		else: break
	return count	
		
def detect_byte(message, blocksize, msglen, initvector):
	charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n-=[];'./,\!@#$%^&*()_+{}|:\"<>? "
	global plaintext
	container = int(math.ceil(float(msglen)/blocksize) * blocksize)
	if initvector == "":
		initvector = "a" * (container - 1) 
	result = encryption_oracle(message, initvector)
	for i in charset:
		fullvector = initvector + plaintext + i
		newresult = encryption_oracle(message, fullvector)
		if result[:container] == newresult[:container]:
			plaintext += i
			if (container - counting(initvector,"a")) ==  msglen: return plaintext
			detect_byte(message, blocksize, msglen, initvector[1:])
			return plaintext
			
if __name__ == "__main__":
	secret = open("simple_ecb_decrypt.txt","r").read()
	message = "".join(line.strip() for line in secret)	
	blocksize = detect_block_size(message)
	detect_mode(message, blocksize)
	length = detect_message_length(message, blocksize)
	print ("Founded Message is: \n", detect_byte(message, blocksize, length,""))

	
	
