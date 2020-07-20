from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from this import encoding

def encrypt(key: str, source: str):
	key = key.encode(encoding)
	source = source.encode(encoding)
	key = SHA256.new(key).digest()	# use SHA-256 over our key to get a proper-sized AES key
	init_vector = Random.new().read(AES.block_size)	# initialization vector
	encryptor = AES.new(key, AES.MODE_CBC, init_vector)
	padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
	source += bytes([padding]) * padding
	data = init_vector + encryptor.encrypt(source)  # store the init_vector at the beginning and encrypt
	return b64encode(data).decode(encoding)

def decrypt(key: str, source: str):
	key = key.encode(encoding)
	source = b64decode(source.encode(encoding))
	key = SHA256.new(key).digest()
	init_vector = source[:AES.block_size]	# extract the init_vector from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, init_vector)
	data = decryptor.decrypt(source[AES.block_size:])
	padding = data[-1]	# pick the padding value from the end
	if data[-padding:] != bytes([padding]) * padding:
		raise ValueError('Invalid padding.')
	return data[:-padding].decode(encoding)	# remove the padding
