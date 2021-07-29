import aescbc
import os
import random
from datetime import datetime


def randomize():
	return os.urandom(16)

def encryption_oracle(message):
	message = os.urandom(random.randint(5,10)) + message + os.urandom(random.randint(5,10))
	#print len(message)
	#print len(aescbc.pkcs7padding(message))
	if random.randint(1,2) == 1:
		print ("Encrypt using ECB")
		return aescbc.aes_128_encrypt_ecb(aescbc.pkcs7padding(message),randomize())
	else:
		print ("Encrypt using CBC")
		return aescbc.aes_128_encrypt_cbc(message,randomize(),randomize())

def detect_mode():
	initvector = "1"*64
	result = encryption_oracle(initvector)
	chunks = list(map(''.join, zip(*[iter(result)]*16)))
	for chunk in chunks:
		if chunks.count(chunk) >= 3:
			print ("ECB detected")
			return
	print ("CBC detected")
	

if __name__ == "__main__":
	random.seed(datetime.now())
	detect_mode()
	
	
