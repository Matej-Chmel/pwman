import os

class WrongUsage(Exception):
	def __init__(self, message):
		super().__init__(message)

class this:
	running = True

CWD = os.getcwd()

def data(file_name):
	return os.path.join(CWD, 'data', file_name)
def res(file_name):
	return os.path.join(CWD, 'res', file_name)

CIPHER_PATH = data('ciphertext.aes')
PLAIN_PATH = data('plaintext.txt')

all_encodings = None
encoding = 'utf_8'

with open(res('encodings.pydef'), 'r') as file:
	all_encodings = eval(file.read())
