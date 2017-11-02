def validation(message, blocksize = 16):
	padbyte = ord(message[-1])
	for i in range(len(message)-padbyte,len(message)):
		print padbyte, ord(message[i])
		if ord(message[i]) != padbyte:
			raise Exception("Not a valid padded string")
			return
	print "This is a valid PKCS7 padded string"

if __name__ == "__main__":
	message1 = "ICE ICE BABY\x04\x04\x04\x04"
	message2 = "ICE ICE BABY\x05\x05\x05\x05"
	message3 = "ICE ICE BABY\x01\x02\x03\x04"
	#validation(message1)
	#validation(message2)
	validation(message3)
