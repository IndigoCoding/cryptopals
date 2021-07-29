from Crypto.Cipher import AES
from binascii import a2b_base64
import os

def aes_128_encrypt_ecb(message, key):
	cipher = AES.new(key,AES.MODE_ECB)
	return cipher.encrypt(message)

def aes_128_decrypt_ecb(message, key):
	cipher = AES.new(key,AES.MODE_ECB)
	return cipher.decrypt(message)

def pkcs7padding(message, size=16):
	padvalue = size - len(message)%size
	return message + chr(padvalue)*padvalue

def pkcs7depadding(message):
	padvalue = ord(message[len(message)-1])
	return message[:len(message)-padvalue]

def xor(a , b):
	if len(b) > len(a):
		a,b = b,a
	return ''.join(chr(ord(a[i])^ord(b[i%len(b)])) for i in range(len(a)))

def aes_128_encrypt_cbc(message, key, iv):
	message = pkcs7padding(message)
	chunks = list(map(''.join, zip(*[iter(message)]*16)))	
	cipher = [aes_128_encrypt_ecb(xor(chunks[0],iv),key)]
	for i in range(1,len(chunks)):
		a = aes_128_encrypt_ecb(xor(chunks[i],cipher[i-1]),key)
		cipher.append(a)
	return ''.join(c for c in cipher)

def aes_128_decrypt_cbc(cipher, key, iv):
	chunks = list(map(''.join, zip(*[iter(cipher)]*16)))	
	plain = [xor(aes_128_decrypt_ecb(chunks[0],key),iv)]
	for i in range(1,len(chunks)):
		plain.append(xor(aes_128_decrypt_ecb(chunks[i],key),chunks[i-1]))
	return pkcs7depadding(''.join(p for p in plain))

if __name__ == "__main__":
	data = a2b_base64(''.join(line.strip() for line in open("message10.txt")))
	key = "YELLOW SUBMARINE"
	#key = "\x42" * 24
	iv = "\x00"*16
	
	print(aes_128_decrypt_cbc(data,key,iv))

