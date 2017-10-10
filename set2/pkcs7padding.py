def padding(string, wantedbyte):
	padvalue = wantedbyte - len(string)
	return string + chr(padvalue)*padvalue

if __name__ == "__main__":
	print repr(padding("YELLOW SUBMARINE",20))
