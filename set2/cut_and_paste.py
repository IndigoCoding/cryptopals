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
		decoded[entry.split('=')[0]]=entry.split('=')[1]
	return decoded

def encode(profile):
	encoded = ""
	for entry in profile:
		encoded += str(entry) + '=' + str(profile[entry]) + '&'
	encoded = encoded[:len(encoded)-1]
	return encoded

def profile_for(email):
	if "&" in email or "=" in email:
		print "Invalid character in email"
		return ""
	uid = random.randint(1,100)
	profile = OrderedDict([("email",email) , ("uid",uid), ("role","user")])
	return encode(profile)
	
def encrypt_profile(profile,key):
	return aescbc.aes_128_encrypt_ecb(aescbc.pkcs7padding(profile),key)

def decrypt_profile(profile,key):
	return parse(aescbc.pkcs7depadding(aescbc.aes_128_decrypt_ecb(profile,key)))

if __name__ == "__main__":
	key = os.urandom(16)
	email = raw_input('Email: ')
	cookie = encrypt_profile(profile_for(email),key)
	print 'Cookie: ',repr(cookie)
	
