from aescbc import *
import os
import random
import time
from datetime import datetime
import math

def randomize():
        return os.urandom(16)

key = randomize()
iv = randomize()

def encryption(userdata):
	global key,iv
	message = userdata.replace("=","?")
	message = message.replace(";","?")
	#print message
	comment1 = "comment1=cooking%20MCs;userdata=" 
	comment2 = ";comment2=%20like%20a%20pound%20of%20bacon"
	message = comment1 + message + comment2
	#print message
	return aes_128_encrypt_cbc(message, key, iv)

def check(userdata):
	global key,iv
	comment1 = "comment1=cooking%20MCs;userdata="
        comment2 = ";comment2=%20like%20a%20pound%20of%20bacon"
	return (comment1 + userdata + comment2)== aes_128_decrypt_cbc(encryption(userdata), key, iv)

def checkadmin(cipher):
	global key,iv
	plain = aes_128_decrypt_cbc(cipher, key, iv)
	for item in plain.split(';'):
		print item
		subitem = item.split('=')
		print subitem[0],subitem[1]
		if subitem[0] == 'admin' and subitem[1] == 'true':
			return True
	return False

def bitflipping():
	blocksize = 16
	positions = [32,38]
	payload = "aadminatrue"
	characters = [';','=']
	newcipherchar = []
	cipher = encryption(payload)
	for i in range(2):
		newcipherchar.append(chr(ord(cipher[positions[i]-blocksize]) ^ ord('a') ^ ord(characters[i])))
	newcipher = cipher[:positions[0]-blocksize] + newcipherchar[0] + cipher[positions[0]+1-blocksize:positions[1]-blocksize] + newcipherchar[1] + cipher[positions[1]+1-blocksize:]
	return newcipher
	
	
if __name__ == "__main__":
	print checkadmin(bitflipping())
