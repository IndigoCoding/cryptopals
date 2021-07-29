import aescbc
import random
import os
import simple_ecb_decrypt
from collections import OrderedDict

def parse(encoded):
	if encoded == "": return OrderedDict()
	lst = encoded.split('&')
	decoded = OrderedDict()
	for entry in lst:
		lst1 = entry.split('=')
		if len(lst1) > 1:
			decoded[lst1[0]]=lst1[1]
		else:
			decoded[lst1[0]]=""
	return decoded

def encode(profile):
	encoded = ""
	for entry in profile:
		encoded += str(entry) + '=' + str(profile[entry]) + '&'
	encoded = encoded[:len(encoded)-1]
	return encoded

def profile_for(email):
	if "&" in email or "=" in email:
		print ("Invalid character in email")
		return ""
	uid = 10
	profile = OrderedDict([("email",email) , ("uid",uid), ("role","user")])
	return encode(profile)
	
def encrypt_profile(profile,key):
	return aescbc.aes_128_encrypt_ecb(aescbc.pkcs7padding(profile),key)

def decrypt_profile(profile,key):
	return aescbc.pkcs7depadding(aescbc.aes_128_decrypt_ecb(profile,key))

def get_block(blocks, blocksize, blocknumber):
	return blocks[blocknumber*blocksize:(blocknumber+1)*blocksize]

def check_admin(profile):
	if parse(profile)['role'] == 'admin' : return True
	return False

if __name__ == "__main__":
	key = os.urandom(16)
	blocksize = 16

	email1 = "x"*13
	email2 = "x"*10 + "admin"
	email3 = "x"*9
	
	blocks1 = encrypt_profile(profile_for(email1),key)
	blocks2 = encrypt_profile(profile_for(email2),key)
	blocks3 = encrypt_profile(profile_for(email3),key)
	
	payload = get_block(blocks1, blocksize, 0) + get_block(blocks1, blocksize, 1) + get_block(blocks2, blocksize, 1) + get_block(blocks3, blocksize, 2)
	
	#print (decrypt_profile(payload,key))
	if check_admin(decrypt_profile(payload,key)):
		print ("(+)Hack successfully. The obtained profile is ",decrypt_profile(payload,key))
	else:
		print ("(+)Hack failed")
		
