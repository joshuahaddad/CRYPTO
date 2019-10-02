import base64

x = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
y = input("Hex>64(1) or 64>Hex(2)")

if(y == 1):
	print(x.decode('hex').encode('base64'))
if(y == 2):
	print(x.decode('base64').encode('hex'))