import binascii

decode = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode('hex')
for i in range(256):
	s = ''
	for b in decode:
		s += (chr(ord(b) ^ i))
	print(s)
